class ProductNotAvailable(Exception):

    def __init__(self, product):
        self.product = product
        msg = "Продукт {} нет в наличии."
        super().__init__(msg.format(product.product_code))