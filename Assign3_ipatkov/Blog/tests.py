from django.test import TestCase
from Blog.models import MyBlog
from datetime import datetime
from django.contrib.auth.models import User

# Create your tests here.
class TestMyBlog(TestCase):
    
    fixtures = ["initial_data.json"]
    
    @classmethod
    def setUpClass(cls):
        blogs=MyBlog.objects.all()
        
        #print blogs
        
        if blogs:
            cls.blog_id=blogs[0].id
        else:
            cls.blog_id = -1 
        
    def setUp(self):
        self.user = User.objects.create_user("hom", "hom")
        self.user.firstname = "John"
        self.user.lastname = "Smith"
        self.user.set_password('hom')
        self.user.save()
    
    def test_cannot_edit_without_login(self):
        print " Testing: ask login before editing and editing "
        assert(TestMyBlog.blog_id != -1)
        
        resp = self.client.get('/editblog/' + str(TestMyBlog.blog_id) + '/')
        self.assertRedirects(resp, '/login/?next=/editblog/' + str(TestMyBlog.blog_id) +'/') 
        
        post_data = {
            'username': 'hom',
            'password': 'hom',
        }  
               
        resp = self.client.post('/login/?next=/editblog/' + str(TestMyBlog.blog_id) + '/', 
                                post_data)
        #self.assertEqual(resp.status_code, 200)
        self.assertRedirects(resp, '/editblog/' + str(TestMyBlog.blog_id) + '/')
    