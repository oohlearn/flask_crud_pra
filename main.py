from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float, Column



app = Flask(__name__)
# 設置應用程式配置以連接到 SQLite 資料庫
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"


# 定義一個基礎的資料庫模型類 Base，繼承自 DeclarativeBase
class Base(DeclarativeBase):
    pass

# 建立 SQLAlchemy 物件 db，並將 Base 作為 model_class 參數傳遞給它
db = SQLAlchemy(model_class=Base)

# 初始化 SQLAlchemy 應用程式
db.init_app(app)

# 定義一個書籍資料模型 Book，繼承自 db.Model，並指定資料表名稱為 "books"
class Book(db.Model):
    __tablename__ = "books"
    id = Column(Integer,  primary_key=True)
    title = Column(String(250), unique=True, nullable=False)
    author = Column(String(250), nullable=False)
    rating = Column(Float, nullable=False)
    


@app.route("/")
def home():
    all_books = Book.query.all()
    return render_template("index.html", all_books = all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title=request.form["title"]
        author=request.form["author"]
        rating=request.form["rating"]
        new_book = Book(title=title, author=author, rating=rating)

        # 建立一本新書的資料紀錄，並將它添加到資料庫中
        db.session.add(new_book)
        # 提交資料庫的變更，以保存新書的資料紀錄
        db.session.commit()   
        return redirect(url_for("home"))        
    return render_template("add.html")

@app.route("/edit/<id>", methods=["GET", "POST"])
def edit(id):
    book_id = id
    book_to_update = db.get_or_404(Book, book_id)
    if request.method == "POST":
        book_to_update.rating = request.form["rating"]
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("edit.html", book = book_to_update)

@app.route("/<id>", methods=["POST"])
def delete(id):
    book_id = id
    book_to_delete = db.get_or_404(Book, book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == "__main__":
    # 在應用程式上下文中執行 db.create_all()，這將創建所有的資料庫表格，如果它們還不存在的話
    with app.app_context():
        # 加上with這行，就可以不管前後順序，避免db還沒創建，無法執行add等跟db扯上關係的功能
        db.create_all()
    app.run(debug=True)
