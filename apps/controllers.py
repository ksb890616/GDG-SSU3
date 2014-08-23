# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for
from sqlalchemy import desc
from apps import app, db

from apps.models import Article, Comment

@app.route('/', methods=['GET'])
def article_list():
	# html 파일에 전달할 데이터 Context
	context = {}
	context["article_list"] = Article.query.order_by(desc(Article.date_created)).all()

	# Article 데이터 전부를 받아와서 최신글 순서대로 정렬하여 'article_list' 라는 key값으로 context에 저장한다.

	return render_template('home.html', context=context)


@app.route('/article/create/', methods=['GET', 'POST'])
def article_create():
	if request.method == 'POST':
		a_data = request.form

		article = Article(
			title = a_data['title'],
			author = a_data['author'],
			category = a_data['category'],
			content = a_data['content']
		)
		#데이터베이스에 데이터를 저장할 준비를한다(게시글)

		db.session.add(article)
		#데이터베이스에 저장하라는 명령을 한다 확정.
		db.session.commit()

		return redirect(url_for('article_list'))


	
	return render_template('article/create.html')


@app.route('/article/detail/<int:id>', methods=['GET'])
def article_detail(id):
	
	article = Article.query.get(id)
	comment = Comment.query.order_by(desc(Comment.date_created)).filter_by(article_id=article.id)

	return render_template('article/detail.html', article=article, comment = comment)


@app.route('/article/delete/<int:id>', methods=['GET', 'POST'])
def article_delete(id):
	if request.method == 'POST' :
		
		article = Article.query.get(id)
		db.session.delete(article)
		db.session.commit()
		# 1. 자신이 삭제하고자 하는 데이터만 DB에서 불러온다.
		# 2. 불러온 데이터를 삭제하고 확정한다.

		return redirect(url_for('article_list'))

	return render_template('article/delete.html', article_id = id)


@app.route('/article/update/<int:id>', methods=['GET', 'POST'])
def article_update(id):
	article = Article.query.get(id)

	if request.method == 'POST':

		b_data = request.form

		article.title = b_data['title']
		article.author = b_data['author']
		article.category = b_data['category']
		article.content = b_data['content']

		# 1. html파일에서 넘어온 데이터를 변수에 저장한다.
		# 2. 불러온 데이터(article)에 내가 수정한 데이터(html파일에서 넘어온 데이터)를 저장한다.
		# 3. DB에 적용되도록 확정한다.
		db.session.commit()

		return redirect(url_for('article_detail', id=id))


	return render_template('article/update.html', article=article)


@app.route('/comment/create/<int:id>', methods=['GET', 'POST'])
def comment_create(id):
	
	if request.method == 'POST':
		c_data = request.form

		comment = Comment(
			article_id = id,
			author = c_data['author'],
			email = c_data['email'],
			password = c_data['password'],
			content = c_data['content']
		)
		#데이터베이스에 데이터를 저장할 준비를한다(게시글)

		db.session.add(comment)
		#데이터베이스에 저장하라는 명령을 한다 확정.
		db.session.commit()
		return redirect(url_for('article_detail', id=id))

	return render_template('comment/create.html')


@app.route('/comment/delete/<int:id>', methods=['GET', 'POST'])
def comment_delete(id):
	if request.method == 'POST':
		comment = Comment.query.get(id)
		if  request.form['password'] == comment.password:
			comment = Comment.query.get(id)
			db.session.delete(comment)
			db.session.commit()
			return redirect(url_for('article_list'))
		else:
			return render_template('comment/wrongpw.html')
		

	return render_template('comment/delete.html', article_id = id)



@app.route('/article/like/<int:id>', methods=['GET', 'POST'])
def article_like(id):
	article = Article.query.get(id)

	article.like += 1
		
	db.session.commit()

	return redirect(url_for('article_detail', id = id))
