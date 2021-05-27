class OutOfStockException(Exception):
    """Exception raised for errors in the input salary."""

    def __str__(self):
        return 'Ürün Stokta yok'
