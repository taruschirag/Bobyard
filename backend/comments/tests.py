from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Comment


class CommentApiTests(APITestCase):
    def test_create_comment_sets_admin_and_timestamp(self):
        url = reverse('comment-list-create')
        response = self.client.post(url, {'text': 'New comment'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['author'], 'Admin')
        self.assertEqual(response.data['text'], 'New comment')
        self.assertIn('date', response.data)
        self.assertEqual(response.data['likes'], 0)

    def test_update_comment_text_only(self):
        comment = Comment.objects.create(author='User', text='Original', likes=1)
        url = reverse('comment-detail', args=[comment.id])
        response = self.client.patch(url, {'text': 'Updated'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        comment.refresh_from_db()
        self.assertEqual(comment.text, 'Updated')
        self.assertEqual(comment.author, 'User')
        self.assertEqual(comment.likes, 1)

    def test_delete_comment(self):
        comment = Comment.objects.create(author='User', text='To delete')
        url = reverse('comment-detail', args=[comment.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0)
