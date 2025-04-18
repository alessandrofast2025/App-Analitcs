import requests
from bs4 import BeautifulSoup
import re
from collections import Counter

class MenuAnalyzer:
    def __init__(self, url):
        self.url = url
        self.menu_data = None
        self.platform = self._detect_platform()
        
    def _detect_platform(self):
        """Detect which delivery platform the URL belongs to"""
        if 'ifood' in self.url.lower():
            return 'iFood'
        elif 'ubereats' in self.url.lower():
            return 'Uber Eats'
        elif 'rappi' in self.url.lower():
            return 'Rappi'
        else:
            return 'Desconhecido'
    
    def _fetch_menu(self):
        """Fetch the menu data from the URL"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(self.url, headers=headers)
        response.raise_for_status()
        return response.text
    
    def _parse_menu(self, html_content):
        """Parse the menu data from HTML content based on the platform"""
        soup = BeautifulSoup(html_content, 'html.parser')
        menu_items = []
        
        if self.platform == 'iFood':
            # iFood specific parsing
            categories = soup.find_all('div', class_=re.compile('dish-card'))
            for item in categories:
                try:
                    name = item.find('h3').text.strip() if item.find('h3') else ''
                    description = item.find('p', class_=re.compile('description')).text.strip() if item.find('p', class_=re.compile('description')) else ''
                    price = item.find('span', class_=re.compile('price')).text.strip() if item.find('span', class_=re.compile('price')) else ''
                    
                    menu_items.append({
                        'name': name,
                        'description': description,
                        'price': price,
                        'image_url': item.find('img')['src'] if item.find('img') and 'src' in item.find('img').attrs else ''
                    })
                except Exception:
                    continue
        
        elif self.platform == 'Uber Eats':
            # Uber Eats specific parsing
            items = soup.find_all('div', {'data-testid': re.compile('menu-item')})
            for item in items:
                try:
                    name = item.find('h4').text.strip() if item.find('h4') else ''
                    description = item.find('p').text.strip() if item.find('p') else ''
                    price_elem = item.find('span', string=re.compile(r'R\$'))
                    price = price_elem.text.strip() if price_elem else ''
                    
                    menu_items.append({
                        'name': name,
                        'description': description,
                        'price': price,
                        'image_url': item.find('img')['src'] if item.find('img') and 'src' in item.find('img').attrs else ''
                    })
                except Exception:
                    continue
        
        # Generic fallback parsing if platform-specific parsing fails
        if not menu_items:
            # Look for common menu item patterns
            items = soup.find_all(['div', 'li'], class_=re.compile('(item|dish|product|menu)'))
            for item in items:
                try:
                    name = item.find(['h2', 'h3', 'h4']).text.strip() if item.find(['h2', 'h3', 'h4']) else ''
                    description = item.find('p').text.strip() if item.find('p') else ''
                    price = item.find(string=re.compile(r'R\$\s*\d+')).strip() if item.find(string=re.compile(r'R\$\s*\d+')) else ''
                    
                    if name:  # Only add if we at least have a name
                        menu_items.append({
                            'name': name,
                            'description': description,
                            'price': price,
                            'image_url': item.find('img')['src'] if item.find('img') and 'src' in item.find('img').attrs else ''
                        })
                except Exception:
                    continue
        
        return menu_items
    
    def analyze(self):
        """Analyze the menu and return improvement suggestions"""
        html_content = self._fetch_menu()
        self.menu_data = self._parse_menu(html_content)
        
        if not self.menu_data:
            raise ValueError("Não foi possível extrair itens do menu. A estrutura do site pode ter mudado ou a URL não é suportada.")
        
        analysis = {
            'platform': self.platform,
            'total_items': len(self.menu_data),
            'suggestions': self._generate_suggestions(),
            'sample_items': self.menu_data[:5]  # Include a few sample items for reference
        }
        
        return analysis
    
    def _generate_suggestions(self):
        """Generate improvement suggestions based on menu analysis"""
        suggestions = []
        
        # Check for missing descriptions
        items_without_description = [item['name'] for item in self.menu_data if not item['description']]
        if items_without_description:
            suggestions.append({
                'type': 'missing_descriptions',
                'title': 'Adicione descrições aos itens',
                'description': f'Encontramos {len(items_without_description)} itens sem descrição. Adicionar descrições detalhadas pode aumentar as vendas em até 30%.',
                'affected_items': items_without_description[:5],  # Show just a few examples
                'affected_count': len(items_without_description)
            })
        
        # Check for missing images
        items_without_images = [item['name'] for item in self.menu_data if not item['image_url']]
        if items_without_images:
            suggestions.append({
                'type': 'missing_images',
                'title': 'Adicione imagens aos itens',
                'description': f'Encontramos {len(items_without_images)} itens sem imagens. Pratos com imagens atraentes têm 65% mais chances de serem pedidos.',
                'affected_items': items_without_images[:5],
                'affected_count': len(items_without_images)
            })
        
        # Check for very short descriptions (less than 10 characters)
        items_with_short_desc = [item['name'] for item in self.menu_data 
                                if item['description'] and len(item['description']) < 10]
        if items_with_short_desc:
            suggestions.append({
                'type': 'short_descriptions',
                'title': 'Melhore as descrições curtas',
                'description': f'Encontramos {len(items_with_short_desc)} itens com descrições muito curtas. Descrições detalhadas ajudam o cliente a tomar decisões.',
                'affected_items': items_with_short_desc[:5],
                'affected_count': len(items_with_short_desc)
            })
        
        # Check for duplicate or very similar items
        names = [item['name'].lower() for item in self.menu_data]
        duplicates = [name for name, count in Counter(names).items() if count > 1]
        if duplicates:
            suggestions.append({
                'type': 'duplicate_items',
                'title': 'Revise itens duplicados ou muito similares',
                'description': f'Encontramos {len(duplicates)} nomes de itens duplicados. Isso pode confundir os clientes.',
                'affected_items': duplicates[:5],
                'affected_count': len(duplicates)
            })
        
        # Check for price clustering
        prices = []
        for item in self.menu_data:
            price_text = item['price']
            if price_text:
                # Extract numeric price value
                price_match = re.search(r'(\d+[.,]\d+)', price_text.replace('R$', ''))
                if price_match:
                    try:
                        price = float(price_match.group(1).replace(',', '.'))
                        prices.append(price)
                    except ValueError:
                        pass
        
        if prices:
            avg_price = sum(prices) / len(prices)
            price_range = max(prices) - min(prices)
            
            if price_range < avg_price * 0.5:
                suggestions.append({
                    'type': 'price_clustering',
                    'title': 'Diversifique a faixa de preços',
                    'description': 'Seus preços estão muito agrupados. Considere oferecer opções premium e econômicas para atender diferentes públicos.',
                    'affected_items': [],
                    'affected_count': len(prices),
                    'min_price': min(prices),
                    'max_price': max(prices),
                    'avg_price': avg_price
                })
        
        # Check for menu organization
        if len(self.menu_data) > 15:
            # This is a heuristic - if we can't detect clear categories and there are many items
            suggestions.append({
                'type': 'organization',
                'title': 'Melhore a organização do cardápio',
                'description': 'Seu cardápio tem muitos itens. Certifique-se de que estão bem organizados em categorias claras para facilitar a navegação.',
                'affected_items': [],
                'affected_count': len(self.menu_data)
            })
        
        return suggestions