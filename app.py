from flask import Flask, request, render_template
from facebook import get_fb_group_compound
from instagram import get_insta_compound

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/facebook')
def facebook():
    return render_template('facebook.html')

@app.route('/scrape-fb-group', methods=['POST'])
def scrape_fb_group():
    group_id = request.form['group-id']
    amount = request.form['amount']
    if group_id is None or len(group_id) == 0:
        return render_template('facebook.html')
    print(f'Received data: {group_id}')
    comp_avg = get_fb_group_compound(group_id, amount)
    return render_template('facebook-scrape.html', group_id=group_id, amount=amount, comp_avg=comp_avg)

@app.route('/instagram')
def instagram():
    return render_template('instagram.html')

@app.route('/scrape-insta', methods=['POST'])
def scrape_insta_tag():
    name = request.form['name']
    category = request.form['category']
    amount = request.form['amount']
    if name is None or len(name) == 0:
        return render_template('instagram.html')
    print(f'Received data: {name}')
    comp_avg = get_insta_compound(name, category, amount)
    return render_template('facebook-scrape.html', name=name, category=category, amount=amount, comp_avg=comp_avg)

if __name__ == '__main__':
    app.run(port=3000, debug=True)