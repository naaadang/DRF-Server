from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import Post
from .serializers import PostSerializer
from rest_framework import generics, mixins

# Create your views here.
# class PostListCreateAPIView(APIView):
#     def get(self,request,format=None):
#         posts=Post.objects.all()
#         serializer=PostSerializer(posts,many=True)
#         return Response(serializer.data)
    
#     def post(self,request,format=None):
#         serializer=PostSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

# class PostRetrieveUpdateDestroyAPIView(APIView):
#     def get_object(self,pk):
#         try:
#             return Post.objects.get(pk=pk)
#         except Post.DoesNotExist:
#             raise Http404
        
#     def get(self,request,pk,format=None):
#         post=self.get_object(pk)
#         serializer=PostSerializer(post)
#         return Response(serializer.data)
    
#     def put(self,request,pk,format=None):
#         post=self.get_object(pk)
#         serializer=PostSerializer(post,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self,request,pk,format=None):
#         post=self.get_object(pk)
#         post.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


##mixin 
# class PostListCreateAPIView(mixins.ListModelMixin, mixins.CreateModelMixin,generics.GenericAPIView):
#     queryset=Post.objects.all()
#     serializer_class=PostSerializer

#     def get(self,request,*args,**kwargs):
#         return self.list(request,*args,**kwargs)
    
#     def post(self,request,*args,**kwargs):
#         return self.create(request,*args,**kwargs)
    
# class PostRetrieveUpdateDestroyAPIView(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
#     queryset=Post.objects.all()
#     serializer_class=PostSerializer

#     def get(self,request,*args,**kwargs):
#         return self.retrieve(request,*args,**kwargs)
    
#     def put(self,request,*args,**kwargs):
#         return self.update(request,*args,**kwargs)
    
#     def delete(self,request,*args,**kwargs):
#         return self.destroy(request,*args,**kwargs)
    

##GenericAPI 파생 view 1
# class PostCreateAPIView(generics.CreateAPIView):
#     queryset=Post.objects.all()
#     serializer_class=PostSerializer

# class PostListAPIView(generics.ListAPIView):
#     queryset=Post.objects.all()
#     serializer_class=PostSerializer

# class PostRetrieveAPIView(generics.RetrieveAPIView):
#     queryset=Post.objects.all()
#     serializer_class=PostSerializer

# class PostUpdateAPIView(generics.UpdateAPIView):
#     queryset=Post.objects.all()
#     serializer_class=PostSerializer

# class PostDestroyAPIView(generics.DestroyAPIView):
#     queryset=Post.objects.all()
#     serializer_class=PostSerializer


# class CreateAPIView(mixins.CreateModelMixin,generics.GenericAPIView):
#     def post(self,request,*args,**kwargs):
#         return self.create(request,*args,**kwargs)
    
# class ListAPIView(mixins.ListModelMixin,generics.GenericAPIView):
#     def get(self,request,*args,**kwargs):
#         return self.list(request,*args,**kwargs)

# class RetrieveAPIView(mixins.RetrieveModelMixin,generics.GenericAPIView):
#     def get(self,request,*args,**kwargs):
#         return self.retrieve(request,*args,**kwargs)

# class DestroyAPIView(mixins.DestroyModelMixin,generics.GenericAPIView):
#     def delete(self,request,*args,**kwargs):
#         return self.destroy(request,*args,**kwargs)

# class UpdateAPIView(mixins.UpdateModelMixin,generics.GenericAPIView):
#     def put(self,request,*args,**kwargs):
#         return self.update(request,*args,**kwargs)
    
#     def patch(self,request,*args,**kwargs):
#         return self.partial_update(request,*args,**kwargs)
    


# #GerericAPIView 파생 view 2
# class PostListCreateAPIView(generics.ListCreateAPIView):
#     queryset=Post.objects.all()
#     serializer_class=PostSerializer

# class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset=Post.objects.all()
#     serializer_class=PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset=Post.objects.all()
    serializer_class=PostSerializer

    def list(self, request, *args, **kwargs):
        # queryset = self.filter_queryset(self.get_queryset().order_by('-updated_at'))

        order=request.query_params.get('order')
        if order=='user':
            queryset=self.filter_queryset(self.get_queryset().order_by('user__email'))
        elif order=='updated':
            queryset=self.filter_queryset(self.get_queryset().order_by('-updated_at'))
        else:
            queryset=self.filter_queryset(self.get_queryset())
       
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
