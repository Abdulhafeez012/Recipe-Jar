from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status


class RecipeInformationTestCase(APITestCase):
    def test_post_valid_data(self):
        url = reverse('get_recipe_information')  # Assuming you have a URL name for this view

        # Sample valid data for POST request
        data = {
            'website_url': 'https://tasty.co/recipe/pizza-dough',
            'user_apple_id': 'abed@icloud.com'
        }

        # Make a POST request
        response = self.client.post(url, data, format='json')

        # Assert the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert the response data structure
        self.assertIn('recipe', response.data)
        self.assertIn('categories', response.data)
        self.assertIn('name', response.data['recipe'])
        self.assertIn('picture_url', response.data['recipe'])
        self.assertIn('ingredients', response.data['recipe'])
        self.assertIn('steps', response.data['recipe'])

        # You can further assert the content of response data if needed

    def test_post_missing_data(self):
        url = reverse('get_recipe_information')  # Assuming you have a URL name for this view

        # Missing 'website_url' in data
        data = {
            'user_apple_id': 'abed@icloud.com'
        }

        response = self.client.post(url, data, format='json')

        # Assert the response status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('website_url', response.data['error'])

        # Missing 'user_apple_id' in data
        data = {
            'website_url': 'https://tasty.co/recipe/pizza-dough'
        }

        response = self.client.post(url, data, format='json')

        # Assert the response status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('user_apple_id', response.data['error'])

    def test_post_invalid_user(self):
        url = reverse('get_recipe_information')  # Assuming you have a URL name for this view

        # Non-existent user_apple_id
        data = {
            'website_url': 'https://tasty.co/recipe/pizza-dough',
            'user_apple_id': 'test@icloud.com'
        }

        response = self.client.post(url, data, format='json')

        # Assert the response status code
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('User not found.', response.data['error'])
