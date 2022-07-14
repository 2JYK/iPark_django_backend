from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from community.serializers import ArticleSerializer
from community.serializers import ArticleCommentSerializer

from community.models import Article as ArticleModel
from community.models import ArticleComment as ArticleCommentModel


#게시글 전체 페이지
class CommunityView(APIView):
    def get(self, request):
        if request.id == 1:  
            article = ArticleModel.objects.filter(tag=1).order_by("-created_at")
            serialized_data = ArticleSerializer(article, many=True).data
            return Response(serialized_data, status=status.HTTP_200_OK)
        else:
            article = ArticleModel.objects.filter(tag=2).order_by("-created_at")
            serialized_data = ArticleSerializer(article, many=True).data
            return Response(serialized_data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        data["user"] = request.user.id
        article_serializer = ArticleSerializer(data=data)
        
        if article_serializer.is_valid():
            article_serializer.save()
            return Response(article_serializer.data, status=status.HTTP_200_OK)
        
        return Response({"mseeage": "게시글 작성 실패 !"}, status=status.HTTP_400_BAD_REQUEST)


#게시글 상세 페이지
class CommunityDetailView(APIView):
    def get(self, request, article_id):
        article = ArticleModel.objects.get(id=article_id)
        article.update_counter
        serialized_data = ArticleSerializer(article, many=True).data
        return Response(serialized_data, status=status.HTTP_200_OK)  
    
    def put(self, request, article_id):
        user = request.user.id
        article = ArticleModel.objects.get(id=article_id)

        if article.user.id == user:
            article_serializer = ArticleSerializer(article, data=request.data, partial=True)
            
            if article_serializer.is_valid():
                article_serializer.save()
                return Response(article_serializer.data, status=status.HTTP_200_OK)
        
        return Response({"message": "게시글 작성자가 아닙니다"}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, article_id):
        user = request.user.id
        article = ArticleModel.objects.get(id=article_id)
        
        if article.user.id == user:
            article.delete()
            return Response({"message": "해당 게시글이 삭제 되었습니다."}, status=status.HTTP_200_OK)
        
        return Response({"message": "게시글 작성자가 아닙니다"}, status=status.HTTP_400_BAD_REQUEST)


# 게시글 상세페이지 댓글
class CommentView(APIView):
    def get(self, request, article_id):
        aritcle = ArticleCommentModel.objects.filter(article_id=article_id)
        serialized_data = ArticleCommentSerializer(aritcle, many=True).data

        return Response(serialized_data, status=status.HTTP_200_OK)

    def post(self, request, article_id):
        article = ArticleModel.objects.get(id=article_id)

        data = {
            "user": request.user.id,
            "article": article.id,
            "comment": request.data["comment"]
        }

        article_serializer = ArticleCommentSerializer(data=data)
        if article_serializer.is_valid():
            article_serializer.save()
            return Response({"message": "댓글작성 완료!"}, status=status.HTTP_200_OK)
        
        return Response({"댓글 작성 실패!"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, comment_id):
        comment = ArticleCommentModel.objects.get(id=comment_id)
        comment_serializer = ArticleCommentSerializer(comment, data=request.data, partial=True)

        if comment_serializer.is_valid():
            comment_serializer.save()
            return Response({"message": "수정완료!"}, status=status.HTTP_200_OK)

        return Response({"message": "수정할수 없는 댓글"}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, comment_id):
        user = request.user.id
        comment = ArticleCommentModel.objects.get(id=comment_id)

        if comment.user.id == user:
            comment.delete()
            return Response({"message": "삭제완료!"}, status=status.HTTP_200_OK)
        
        return Response({"message": "삭제할수 없는 댓글"}, status=status.HTTP_400_BAD_REQUEST)