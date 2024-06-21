from app import app
import hostel_bot
import database

if __name__ == '__main__':
    database.init_db()
    from threading import Thread
    print("running")
    Thread(target=hostel_bot.bot.polling, args=(), daemon=True).start()
    app.run(debug=True, port=5000)
