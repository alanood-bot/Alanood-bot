import telebot, ccxt, pandas as pd, pandas_ta as ta, time
from flask import Flask
from threading import Thread

# تشغيل سيرفر ويب صغير لإبقاء الخدمة تعمل على Render
app = Flask('')
@app.route('/')
def home(): return "Bot is Running!"

def run_web(): app.run(host='0.0.0.0', port=8080)

# إعدادات البوت
token = '8389783870:AAHpZkfuEjUF7Nhd7bUyPVovLc24DPr81qI'
bot = telebot.TeleBot(token)
chat_id = -1002331987595
exchange = ccxt.bybit()

symbols = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'BNBUSDT', 'ARBUSDT', 'AVAXUSDT', 'DOGEUSDT']

def main_logic():
    print("🚀 انطلاق الإمبراطور...")
    while True:
        for s in symbols:
            try:
                bars = exchange.fetch_ohlcv(s, timeframe='5m', limit=50)
                df = pd.DataFrame(bars, columns=['time', 'open', 'high', 'low', 'close', 'vol'])
                df['rsi'] = ta.rsi(df['close'], length=14)
                l = df.iloc[-1]
                
                # إشارات الدخول (تم ضبطها لتكون متوازنة)
                if l['rsi'] < 40: sig = "فرصة LONG 📈"
                elif l['rsi'] > 60: sig = "فرصة SHORT 📉"
                else: continue
                
                msg = f"🔥 تحديث إمبراطوري\n💰 العملة: #{s}\n📈 النوع: {sig}\n💵 السعر: {l['close']}\n🎯 مبروك يا العنود ✅"
                bot.send_message(chat_id, msg)
                time.sleep(2)
            except: pass
        time.sleep(60) # استراحة دقيقة للحفاظ على استقرار الخدمة

if __name__ == "__main__":
    t = Thread(target=run_web)
    t.start()
    main_logic()
