from django.db.models import Q

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication

from community.serializers import ArticleSerializer
from community.serializers import ArticleCommentSerializer
from park.serializers import ToggleParkListSerializer

from community.models import Article as ArticleModel
from community.models import ArticleComment as ArticleCommentModel
from park.models import Park as ParkModel

from community.pagination import PaginationHandlerMixin, BasePagination


# 게시글 전체 페이지
#   pagination이 필요한 APIView 클래스에게 PaginationHandlerMixin을 인자로 줌
class CommunityView(APIView, PaginationHandlerMixin):
    authentication_classes = [JWTAuthentication]
    pagination_class = BasePagination   # query_param 설정 : ?page_size=<int>

    def get(self, request):
        id = request.GET.get('id', None)    # query_param 설정 : ?id=<int>

        if id is None:
            article = ArticleModel.objects.all().order_by("-created_at")
            page = self.paginate_queryset(article)  # page_size, page에 따른 pagination 처리된 결과값
            # 페이징 처리된 결과를 serializer에 담아서 결과 값 가공
            serializer = self.get_paginated_response(ArticleSerializer(page, many=True).data)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if int(id) == 1 or int(id) == 2:
            article = ArticleModel.objects.filter(tag=id).order_by("-created_at")
            page = self.paginate_queryset(article)  # page_size, page에 따른 pagination 처리된 결과값
            # 페이징 처리된 결과를 serializer에 담아서 결과 값 가공
            serializer = self.get_paginated_response(ArticleSerializer(page, many=True).data)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if int(id) == 3:
            user = request.user
            if user.is_anonymous:
                return Response({"message": "로그인이 필요한 페이지입니다."}, status=status.HTTP_401_UNAUTHORIZED)    
            article = ArticleModel.objects.filter(user=user).order_by("-created_at")
            page = self.paginate_queryset(article)  # page_size, page에 따른 pagination 처리된 결과값
            # 페이징 처리된 결과를 serializer에 담아서 결과 값 가공
            serializer = self.get_paginated_response(ArticleSerializer(page, many=True).data)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"message": "접근 권한이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        data = request.data.dict()
        data["user"] = request.user.id
        article_serializer = ArticleSerializer(data=data)

        if article_serializer.is_valid():
            article_serializer.save()
            return Response(article_serializer.data, status=status.HTTP_200_OK)

        return Response({"message": "게시글에 빈칸이 있습니다."}, status=status.HTTP_400_BAD_REQUEST)


# park_name 데이터
class ParkOptionView(APIView):
    def get(self, request):
        park = ParkModel.objects.all()
        serialized_data = ToggleParkListSerializer(park, many=True).data
        return Response(serialized_data, status=status.HTTP_200_OK)


# 게시글 검색
class CommunitySearchView(APIView):
    def get(self, request):
        keyword = request.GET["keyword"]
        print(keyword)
        article = ArticleModel.objects.filter(
            Q(title__icontains=keyword) | Q(content__icontains=keyword)
        )
        print(article)
        serialized_data = ArticleSerializer(article, many=True).data
        return Response(serialized_data, status=status.HTTP_200_OK)


#게시글 상세 페이지
class CommunityDetailView(APIView):
    def get(self, request, article_id):
        article = ArticleModel.objects.get(id=article_id)
        article.update_counter
        serialized_data = ArticleSerializer(article).data
        
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
        article = ArticleCommentModel.objects.filter(article_id=article_id)
        serialized_data = ArticleCommentSerializer(article, many=True).data

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
            return Response({"message": "댓글작성 완료!", "data": article_serializer.data}, status=status.HTTP_200_OK)

        return Response({"message": "댓글 작성 실패!"}, status=status.HTTP_400_BAD_REQUEST)

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