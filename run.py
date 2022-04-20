import os
from flask import Flask, render_template, request

from famapy.metamodels.fm_metamodel.transformations import FeatureIDEReader
from fm_characterization.models.fm_characterization import FMCharacterization
from fm_characterization.models import interfaces

app = Flask(__name__,
            static_url_path='', 
            static_folder='web',
            template_folder='web')


FM_FACT_JSON_FILE = 'web/fm_facts.json'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        if os.path.exists(FM_FACT_JSON_FILE):
            os.remove(FM_FACT_JSON_FILE)

        return render_template('index.html')

    if request.method == 'POST':
        data = {}

        name = request.form['inputName']
        description = request.form['inputDescription']
        author = request.form['inputAuthor']
        reference = request.form['inputReference']
        keywords = request.form['inputKeywords']
        fm_file = request.files['inputFM']

        print(f'name: {name}')
        print(f'description: {description}')
        print(f'author: {author}')
        print(f'reference: {reference}')
        print(f'keywords: {keywords}')
        print(f'fm_file: {fm_file}')

        if not fm_file:
            pass

        if fm_file:
            filename = fm_file.filename
            try:
                fm_file.save(filename)
                
                fm = FeatureIDEReader(filename).transform() 
                if not name:
                    name = os.path.splitext(os.path.basename(filename))[0]
                
                fm_characterization = FMCharacterization(fm, name)
                interfaces.to_json(fm_characterization, FM_FACT_JSON_FILE)
            except:
                data['fm_facts'] = False
                os.remove(filename)

        data['fm_facts'] = True
        return render_template('index.html', data=data)


# if __name__ == '__main__':
#     app.debug = True
#     app.run(host='0.0.0.0', port=5555)

if __name__ == '__main__':
    app.run()