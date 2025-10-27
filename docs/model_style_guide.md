# Django Model Template (ASCENSION Project Standard)

## Structure Order
1. Fields
2. Meta
3. Validation methods (clean)
4. Save/Delete overrides
5. Custom methods
6. __str__ (last)

## Example Template
```python
class BaseModel(models.Model):
    """
    Abstract base model that provides common fields and structure.
    All project models should follow this structure for consistency.
    """

    # ===== Basic timestamp fields =====
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # Do not create a table for BaseModel
        ordering = ["-created_at"]  # Default ordering for all child models
        # verbose_name = "Base model"
        # verbose_name_plural = "Base models"

    # ===== Validation =====
    def clean(self):
        """
        Perform model-level validation before saving.
        Raise ValidationError if any rule is violated.
        """
        super().clean()

    # ===== Save / Delete overrides =====
    def save(self, *args, **kwargs):
        """
        Override save() to add custom pre-save logic.
        Always call super() to ensure Django's default behavior.
        """
        # Example: Ensure updated_at is refreshed
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Override delete() to handle custom pre/post deletion logic.
        """
        super().delete(*args, **kwargs)

    # ===== Custom / business logic =====
    def is_recent(self):
        """Return True if created within the last 7 days."""
        return (timezone.now() - self.created_at).days < 7

    # ===== String representation =====
    def __str__(self):
        """Readable name for admin and shell."""
        return f"{self.__class__.__name__} (id={self.pk})"