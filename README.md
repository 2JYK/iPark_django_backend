# iPark Project
frontend repo -> https://github.com/2JYK/iPark_frontend<br>

## 프로젝트 개요
- 공원을 중심으로 한 지역의 커뮤니티 구성
- 커뮤니티를 통해 친목 도모 및 나눔마켓 활성화
- 공원 옵션 또는 선호 지역을 선택해 원하는 공원 찾기

<br>

# ⚙ 개발환경
## back-end : <img src="https://img.shields.io/badge/python-3.9.10-3776AB?style=for-the-badge&logo=python&logoColor=white"> <img src="https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white">

## front-end : <img src="https://img.shields.io/badge/html5-E34F26?style=for-the-badge&logo=html5&logoColor=white"> <img src="https://img.shields.io/badge/css-1572B6?style=for-the-badge&logo=css3&logoColor=white"> <img src="https://img.shields.io/badge/javascript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black"> <img src="https://img.shields.io/badge/jquery-0769AD?style=for-the-badge&logo=jquery&logoColor=white">

## deploy : <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=Docker&logoColor=white"> <img src="https://img.shields.io/badge/amazonaws-232F3E?style=for-the-badge&logo=amazonaws&logoColor=white">
## API : 
- SearchParkInfoService | Seoul OpenAPI
- NAVER Maps JavaScript API V3
- REST API | Kakao
<br>

# 🚀 역할

### 전체 역할
![역할](https://user-images.githubusercontent.com/89643366/182292718-d8d7c112-19dd-4550-bb73-7c6ce97cc63b.png)

<br>

# 🕸 와이어 프레임
<details>
<summary> Click ! </summary>
<div markdown="1">

## user
![image](https://user-images.githubusercontent.com/89643366/182296112-acce2c07-39a4-4f3b-99bb-88273296213f.png) 
## park
![image](https://user-images.githubusercontent.com/89643366/182296589-74757ba1-0688-4f4d-8690-90bc36c5d409.png)
## community
![image](https://user-images.githubusercontent.com/89643366/182296310-2842b5d6-2f46-471f-a380-c4e8e19398cb.png)
</div>
</details>

<br>

# 🎈 기능 명세서
<details>
<summary> 메인페이지 </summary>
<div markdown="1">

- 상단바
    - 네비게이션을 통해 해당 페이지로 이동 또는 로그인/로그아웃을 할 수 있음
        - 공원 상세 페이지
        - 커뮤니티 페이지
        - 계정관리 페이지
        - 로그인/로그아웃
    - 토글
        - 공원 클릭시 공원 상세 내용 페이지로 이동
        - 기본값으로 가나다순으로 공원 정렬
    - 즐겨찾기
        - 관심있는 공원 목록을 확인할 수 있음
    - 내가 쓴 게시글
        - 커뮤니티에서 작성한 게시글들을 조회할 수 있음
- 공원 검색 버튼을 눌러 공원 검색 페이지로 이동해 원하는 조건의 공원을 찾을 수 있음
- 커뮤니티 버튼을 눌러 커뮤니티 페이지로 이동하여 게시글을 조회,작성할 수 있음

</div>
</details>

<br>

<details>
<summary> 로그인 페이지 </summary>
<div markdown="1">

- 로그인
    - 카카오 계정 혹은 가입한 아이디로 로그인
    - 로그인에 성공하면 <span style="color: #FFA7A7;">access token, refresh token, payload</span>가  local Storage에 담김
        - payload의 exp를 통해 access token의 만료를 계산
        - 서비스를 이용하는 도중 access token이 만료되면 refresh token을 통해 갱신해주어 사용자가 서비스를 지속적으로 이용할 수 있도록 함
    - 카카오 로그인
        - 팝업을 통해 카카오 로그인을 진행함.
        - 필수 수집항목으로는 username, email 값을 받음
            - 카카오 계정에서의 <span style="color: #FFA7A7;">email, username</span> 값이 데이터베이스에 있을 경우
                - 비밀번호 값이 함께 존재한다면 자동로그인을 시켜주어 token, payload를 local Storage에 담아주고, 메인페이지로 이동
                - 비밀번호 값이 없다면 카카오계정에서 받은 <span style="color: #FFA7A7;">email, username, fullname</span> 값을 회원가입란으로 보내주어 추가적인 회원정보를 입력할 수 있도록 유도
            - 카카오 계정에서의 <span style="color: #FFA7A7;">email, usernameM</span> 값이 데이터베이스에 없을 경우 카카오 팝업을 띄어준 후 카카오 계정값을 받아 회원가입란으로 보내주어 추가적 회원정보를 입력할 수 있도록 유도
- 아이디 찾기
    - 회원가입을 할 때 입력한 정보인 <span style="color: #FFA7A7;">이메일, 핸드폰 번호</span> 확인을 통해 아이디를 찾을 수 있음
    - 가입한 내역이 있는 사용자라면 알림창을 띄어주어 본인의 아이디를 확인시켜줌
- 비밀번호 변경
    - 가입한 아이디와 이메일 확인을 통해 비밀번호를 변경할 수 있음
    - 새로운 비밀번호는 2 번 입력해 제대로 작성되었는지 확인
    - 영어 소문자/숫자/특수문자를 필수적으로 사용해야 하며 8 자리 이상의 형식을 맞춰야 함
- 기존에 가입한 사용자가 아니라면 회원가입 버튼을 눌러 회원가입 페이지로 이동할 수 있음

</div>
</details>

<br>

<details>
<summary> 회원가입 페이지 </summary>
<div markdown="1">

- 회원가입
    - 카카오 계정 혹은 계정 생성으로 간편 가입
        - 카카오 로그인의 경우, 카카오에서 가져온 아이디, 이메일 등의 정보가 자동기입되어 있음
        - 기입되어 있는 정보들을 수정할 수 있으며, 나머지 값들도 입력해야 회원가입이 진행됨
    - 정해진 형식에 맞게 기입해야 회원가입 가능
        - 아이디 : 6 자리 이상
        - 이메일 : 이메일 형식에 맞게 작성 필요
            - <span style="color: #FFA7A7;">naver, google, kakao, daum, nate, outlook</span> 계정만 가입 가능
        - 비밀번호 : 영어 소문자/숫자/특수문자를 필수적으로 사용해야 하며 8 자리 이상
        - 핸드폰 번호 : <span style="color: #FFA7A7;">010-0000-0000</span> 의 형식으로 작성
- 회원가입이 완료되면 로그인 페이지로 이동
- 이미 계정이 있는데 해당 페이지에 들어온 경우 로그인 페이지로 돌아갈 수 있도록 버튼 생성

</div>
</details>

<br>

<details>
<summary> 공원 검색 페이지 </summary>
<div markdown="1">

- 공원 옵션
    - 8 가지의 공원 특성
    - 서울시 25개 자치구
- 공원 옵션을 선택해 사용자가 원하는 조건의 공원을 검색할 수 있음
    - 3 가지의 방법으로 공원을 검색할 수 있음
        - 하나 또는 여러 개의 공원의 특성을 통해 검색 가능
        - 하나 또는 여러 개의 지역을 통해 검색 가능
        - 공원의 특성과 지역을 동시에 선택해 검색 가능
- 가로 스크롤을 이용해 검색된 공원 목록을 확인
- 조회수가 많은 순으로 공원을 사용자에게 제시함
    - 한 번도 조회가 되지 않은 공원은 제시되지 않음

</div>
</details>

<br>

<details>
<summary> 공원 상세 내용 페이지 </summary>
<div markdown="1">

- 공원 상세 정보
    - 공원 이름, 주소, 사진, 시설, 설명, 전화번호, 홈페이지
    - 지도
        - 지도를 움직여 주변 시설들을 확인할 수 있음
        - 지도 내 마커 클릭시, 길찾기 기능을 이용한 공원으로 가는 경로 검색
- 즐겨찾기
    - 즐겨찾기 버튼을 눌러 즐겨찾기 페이지에서 모아볼 수 있음
    - 즐겨찾기 버튼을 다시 누르면 해제됨
- 댓글
    - 해당 공원에 대한 댓글을 이용해 사용자간의 소통이 가능함
    - pagination을 사용해 한 번에 보여주는 댓글의 개수는 10개
    - 댓글의 작성자는 본인의 댓글을 수정, 삭제를 할 수 있음

</div>
</details>

<br>

<details>
<summary> 즐겨찾기 페이지 </summary>
<div markdown="1">

- 사용자가 즐겨찾기한 공원들을 최신순으로 정렬
- 삭제 버튼을 눌러 즐겨찾기한 공원을 삭제
- 공원의 이미지 혹은 이름을 클릭하여 공원의 상세 정보 페이지로 이동

</div>
</details>

<br>

<details>
<summary> 커뮤니티 페이지 </summary>
<div markdown="1">

- 첫 페이지는 전체 게시글로, 모든 사용자들이 작성한 게시글을 보여줌
- 게시판 고르기, 공원고르기(드롭다운)를 클릭하여 해당 게시판을 확인할 수 있음
    - <span style="color: #FFA7A7;"> 커뮤니티 | 나눔마켓 | 내가 쓴 게시글 </span>
    - <span style="color: #FFA7A7"> 선호하는 공원 </span>
- <span style="color: #FFA7A7">업로드</span> 버튼을 클릭하여 게시글 업로드 페이지로 이동
- 글의 제목을 클릭하여 해당 게시글 상세페이지로 이동
- 검색창을 사용하여 게시글 제목, 내용을 포함한 검색결과를 확인할 수 있음
- pagination을 사용해 한 번에 보여주는 페이지의 개수는 13개

</div>
</details>

<br>

<details>
<summary> 게시글 업로드 페이지 </summary>
<div markdown="1">

- 태그 [ 커뮤니티 or 나눔마켓 ]를 선택
- 사진 / 제목 / 내용 기입
    - 사진은 입력하지 않아도 무관
- 업로드 버튼을 누르면 등록 완료 알림이 뜨며 커뮤니티 첫 페이지로 이동
- 작성된 게시글은 <span style="color: #FFA7A7">내가 쓴 게시글</span>에서 확인 가능

</div>
</details>

<br>

<details>
<summary> 게시글 상세페이지 </summary>
<div markdown="1">

- 게시글에 대한 내용을 확인
    - 게시글 태그, 제목, 내용, 작성자, 작성일자, 조회수, 댓글수
- 게시글의 작성자에게는 수정, 삭제 버튼이 보여 해당 기능을 사용할 수 있음
- 게시글 상세페이지로 이동시 조회수 +1
- 댓글
    - 사용자들은 해당 게시글에 대한 댓글을 통해 자유롭게 소통이 가능함
    - 최대 200자 제한
    - 댓글의 작성자는 본인의 댓글을 삭제를 할 수 있음

</div>
</details>

<br>

# 🎯 데이터베이스

<img width="1242" alt="ipark" src="https://user-images.githubusercontent.com/104303285/185301146-12508b43-dd0f-4bd1-afa1-5666f2fab8ea.png">

<br>

# 🎨 API 설계
<img width="959" alt="스크린샷 2022-08-18 오후 1 13 48" src="https://user-images.githubusercontent.com/99387514/185292781-29cb132d-5042-4c6a-a6c9-97a42363df09.png">

<img width="946" alt="스크린샷 2022-08-18 오후 1 19 53" src="https://user-images.githubusercontent.com/99387514/185292957-a321a78f-35e2-415e-898a-319c8ec9ca49.png">

<img width="927" alt="스크린샷 2022-08-18 오후 1 20 09" src="https://user-images.githubusercontent.com/99387514/185292976-b68e1ae6-630c-4bcf-a510-47db46ccd59e.png">

