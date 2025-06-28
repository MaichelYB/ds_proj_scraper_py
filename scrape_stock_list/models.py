from django.db import models

# Create your models here.
class StockList(models.Model):
    symbol = models.CharField(
        max_length=20,
        unique=True,
        help_text="Unique stock ticker symbol (e.g., AAPL)"
    )
    name = models.CharField(
        max_length=100,
        blank=True,
        help_text="Company name"
    )
    exchange = models.CharField(
        max_length=50,
        blank=True,
        help_text="Stock exchange where the stock is listed"
    )
    country = models.CharField(
        max_length=50,
        blank=True,
        help_text="Country of the primary exchange"
    )
    currency = models.CharField(
        max_length=3,
        default="USD",
        help_text="Trading currency"
    )
    asset_type = models.CharField(
        max_length=20,
        choices=[
            ('STOCK', 'Stock'),
            ('ETF', 'ETF'),
            ('INDEX', 'Index'),
            ('CRYPTO', 'Cryptocurrency'),
            ('OTHER', 'Other'),
        ],
        default='STOCK',
        help_text="Type of financial instrument"
    )

    # Additional metadata
    is_active = models.BooleanField(
        default=True,
        help_text="Whether the stock is currently active/traded"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.symbol} ({self.name})" if self.name else self.symbol

    class Meta:
        ordering = ['symbol']  # Default sorting by symbol
        indexes = [
            models.Index(fields=['symbol']),  # Faster lookups
            models.Index(fields=['exchange']),
        ]

