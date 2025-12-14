from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

# Define the 17 UN Sustainable Development Goals as choices
SDG_CHOICES = (
    (1, 'No Poverty'),
    (2, 'Zero Hunger'),
    (3, 'Good Health and Well-being'),
    (4, 'Quality Education'),
    (5, 'Gender Equality'),
    (6, 'Clean Water and Sanitation'),
    (7, 'Affordable and Clean Energy'),
    (8, 'Decent Work and Economic Growth'),
    (9, 'Industry, Innovation, and Infrastructure'),
    (10, 'Reduced Inequality'),
    (11, 'Sustainable Cities and Communities'),
    (12, 'Responsible Consumption and Production'),
    (13, 'Climate Action'),
    (14, 'Life Below Water'),
    (15, 'Life on Land'),
    (16, 'Peace, Justice, and Strong Institutions'),
    (17, 'Partnerships for the Goals'),
)

# --- 1. SDGProject Model (The Main Project Blueprint) ---
class SDGProject(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    # Uses the predefined choices for filtering and consistency
    sdg_goal = models.IntegerField(choices=SDG_CHOICES, default=1)
    
    # Store amounts as Decimal for accurate currency calculation
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    
    # Image field for project thumbnail (optional for now - using URLField for external images)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    
    # Links the project to the user who created it (ForeignKey)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

    # Property for Progress Bar calculation
    @property
    def percentage_funded(self):
        if self.target_amount > 0:
            percentage = (self.current_amount / self.target_amount) * 100
            return min(100, round(percentage, 1))  # Cap at 100%
        return 0
    
    # Property for image URL with fallback
    @property
    def image(self):
        class ImageURL:
            def __init__(self, url):
                self.url = url or '/static/placeholder.png'
        return ImageURL(self.image_url)

# --- 2. Donation Model (The M-Pesa Transaction Blueprint) ---
class Donation(models.Model):
    # Links the donation back to the specific project (ForeignKey)
    project = models.ForeignKey(SDGProject, on_delete=models.CASCADE)
    
    # User is nullable in case we allow anonymous donations
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    # Storing the number for the M-Pesa simulation context
    phone_number = models.CharField(max_length=15) 
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Donation of {self.amount} to {self.project.title}"