
from .models import Item
from collections import Counter


# selecteditems =  [{'name': 'A','quantity': 3}, {'name': 'B','quantity': 2}]

class GenerateBill:
    def __init__(self, selecteditems ):
        self.selecteditems = selecteditems
        self.cart = {}
        self.populate_cart()
    
    def populate_cart(self):
        for item in self.selecteditems:
            item_name = item['name']
            item_quantity = item['quantity']
            
            try:
                item_instance = Item.objects.get(name=item_name)
                self.cart[item_instance] = item_quantity
            except Item.DoesNotExist:
                print(f"Item '{item_name}' does not exist.")

    def calculate_price_item(self, item_instance, count):
        applicable_discounts = item_instance.discounts.all()
        sorted_discounts = sorted(applicable_discounts, key=lambda x: -x.quantity)
        print("sorted_discounts",sorted_discounts)
        remaining_quantity = count
        price_item = item_instance.price
        total_price_item = 0

        for discount in sorted_discounts:
            offer_count = remaining_quantity // discount.quantity
            print("offer_count is ", offer_count," -- ", remaining_quantity )
            if offer_count > 0:
                discounted_price = offer_count * discount.price
                total_price_item += discounted_price
                remaining_quantity %= discount.quantity

        total_price_item += remaining_quantity * price_item
     

        return total_price_item

    def total_price(self):
        print("cart is", self.cart)
      
        total_price = 0
        item_wise_prices = []

        for item_instance, count in self.cart.items():
            price_item = self.calculate_price_item(item_instance, count)
            total_price += price_item
            print("price_item",price_item, " --- " , item_instance.name)
            item_wise_prices.append({
                'name': item_instance.name,
                'quantity': count,
                'total_price': price_item,
            })
        
        return total_price, item_wise_prices

