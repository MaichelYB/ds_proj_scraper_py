from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class StockPrice(models.Model):
    stock = models.ForeignKey(
        'scrape_stock_list.StockList',  # References your Stock model
        on_delete=models.CASCADE,
        related_name='prices'
    )
    
    # Core price data
    date = models.DateField()
    open = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        validators=[MinValueValidator(0)]
    )
    high = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        validators=[MinValueValidator(0)]
    )
    low = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        validators=[MinValueValidator(0)]
    )
    close = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        validators=[MinValueValidator(0)]
    )
    adj_close = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        null=True,
        blank=True,
        help_text="Adjusted close price for corporate actions"
    )
    
    # Volume information
    volume = models.BigIntegerField(
        validators=[MinValueValidator(0)],
        help_text="Number of shares traded"
    )
    
    # Derived metrics
    change_pct = models.DecimalField(
        max_digits=7,
        decimal_places=4,
        null=True,
        blank=True,
        help_text="Percentage change from previous close"
    )
    
    # Metadata
    data_source = models.CharField(
        max_length=30,
        default="Yahoo Finance"
    )
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [['stock', 'date']]  # Prevent duplicate entries
        ordering = ['-date']  # Newest first by default
        indexes = [
            models.Index(fields=['stock', 'date']),  # Optimize time-series queries
            models.Index(fields=['date']),  # Cross-stock analysis
        ]

    def __str__(self):
        return f"{self.stock.symbol} - {self.date}: ${self.close}"