import random
from flask import Flask, render_template, request, redirect, url_for, jsonify
from faker import Faker

fake = Faker()
app = Flask(__name__)

app.config['SERVER_NAME'] = 'pustygina.pythonanywhere.com'

images_ids = [
    '7d4e9175-95ea-4c5f-8be5-92a6b708bb3c',
    '2d2ab7df-cdbc-48a8-a936-35bba702def5',
    '6e12f3de-d5fd-4ebb-855b-8cbc485278b7',
    'afc2cfe7-5cac-4b80-9b9a-d5c65ef0c728',
    'cab5b7f2-774e-4884-a200-0c0180fa777f'
]

def generate_comments(replies=True):
    comments = []
    for _ in range(random.randint(1, 3)):
        comment = {
            'id': random.randint(1, 9999),
            'author': fake.name(),
            'text': fake.text(),
            'date': fake.date_time_between(start_date='-2y', end_date='now'),
            'replies': generate_comments(replies=False) if replies else []
        }
        comments.append(comment)
    return comments

def generate_post(i):
    return {
        'id': i,
        'title': f'Заголовок поста {i+1}',
        'text': fake.paragraph(nb_sentences=100),
        'author': fake.name(),
        'date': fake.date_time_between(start_date='-2y', end_date='now'),
        'image_id': f'{images_ids[i % len(images_ids)]}.jpg',  # Используем модуль для цикла изображений
        'comments': generate_comments()
    }

posts_list = sorted([generate_post(i) for i in range(5)], key=lambda p: p['date'], reverse=True)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts')
def posts():
    return render_template('posts.html', title='Посты', posts=posts_list)

@app.route('/posts/<int:index>')
def post(index):
    # Проверка, чтобы индекс был в пределах доступных постов
    if 0 <= index < len(posts_list):
        p = posts_list[index]
        return render_template('post.html', title=p['title'], post=p, comments=p['comments'])
    return redirect(url_for('posts'))  # Если индекс некорректен, перенаправляем на список постов

@app.route('/about')
def about():
    return render_template('about.html', title='Об авторе')

@app.route('/comment/<int:post_id>', methods=['POST'])
def add_comment(post_id):
    try:
        comment_text = request.form.get('comment_text')

        # Проверка на пустой комментарий
        if not comment_text:
            return jsonify({'error': 'Комментарий не может быть пустым'}), 400

        # Проверяем, что пост существует
        if 0 <= post_id < len(posts_list):
            new_comment = {
                'id': random.randint(1, 9999),
                'author': 'Аноним',
                'text': comment_text,
                'date': fake.date_time_between(start_date='-1d', end_date='now'),
                'replies': []
            }
            post = next((p for p in posts_list if p['id'] == post_id), None)
            post['comments'].insert(0, new_comment)


            # Возвращаем только новый комментарий
            return jsonify({'html': render_template('comments.html', comments=post['comments'], post=post)})

        return jsonify({'error': 'Пост не найден'}), 404

    except Exception as e:
        return jsonify({'error': f'Произошла ошибка: {str(e)}'}), 500


@app.route('/reply/<int:post_id>/<int:comment_id>', methods=['POST'])
def add_reply(post_id, comment_id):
    post = next((p for p in posts_list if p['id'] == post_id), None)

    if post:  # Проверяем, что пост найден
        # Теперь ищем комментарий только в найденном посте
        comment = next((c for c in post['comments'] if c['id'] == comment_id), None)

        if comment:  # Если комментарий найден
            # Добавляем ответ
            new_reply = {
                'id': random.randint(1, 9999),
                'author': 'Аноним',
                'text': request.form.get('reply_text'),
                'date': fake.date_time_between(start_date='-1d', end_date='now')
            }
            comment['replies'].append(new_reply)

            # Возвращаем весь список комментариев с обновленным ответом
            return jsonify({
                'html': render_template('comments.html', comments=post['comments'], post=post)
            })
        else:
            # Если комментарий не найден
            return jsonify({'error': 'Не найден комментарий с таким ID'}), 404
    else:
        # Если пост не найден
        return jsonify({'error': 'Не найден пост с таким ID ' + str(post_id)}), 404

if __name__ == '__main__':
    app.run(debug=True)
