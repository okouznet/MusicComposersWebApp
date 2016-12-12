from flask import *
import PianoPlayer
import os

app = Flask(__name__)

piano = PianoPlayer.PianoPlayer()
colors = ["Teal", "MediumSeaGreen", "Maroon", "Chocolate", "SandyBrown", "Gold", "OliveDrab"]

#home page
@app.route('/')
def homepage():
    return render_template('index.html')

#settings page
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    piano.clearTrack()
    return render_template('settings.html')

#compose page
#compose page
@app.route('/compose', methods=['GET', 'POST'])
def compose():
    if request.method == 'POST':
        #if saving file
        save = int(request.form["save"])
        if (save == 1):
            filename = str(request.form["file"])
            piano.saveTrack(filename=filename)
            piano.clearTrack()
        else:
            note = request.form.getlist('note[]')
            if len(note) > 0:
                n = []
                for i in note:
                    n.append(int(i))
                n = list(set(n))
                piano.addTrack(notes=n)
        return render_template('compose.html')
    else:
        whitekeys = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        blackkeys = ['C#', 'D#', 'F#', 'G#', 'A#']
        options = {
            "whitekeys": whitekeys,
            "blackkeys": blackkeys,
            "i": 'D#'
        }
        return render_template('compose.html', **options)

#play page
@app.route('/play', methods=['GET','POST'])
def play():
    piano.clearTrack()
    chopin = piano.make_queue(filename="static/playback/chopin_fantasie_imp.mid")
    piano.clearTrack()
    furelise = piano.make_queue(filename="static/playback/for_elise_by_beethoven.mid")
    piano.clearTrack()
    moonlight = piano.make_queue(filename="static/playback/moonlight_sonata.mid")
    piano.clearTrack()
    music = [furelise, chopin, moonlight]
    if request.method == 'POST':
        return render_template('play.html')
    else:
        whitekeys = ['C', 'D', 'E', 'F', 'G', 'A', 'B']

        blackkeys = ['C#', 'D#', 'F#', 'G#', 'A#']

        options = {
            "music": music,
            "whitekeys": whitekeys,
            "blackkeys": blackkeys,
            "i": 'D'
        }
        return render_template('play.html', **options)

#edit page
@app.route('/edit', methods=['GET', 'POST'])
def edit():
    piano.clearTrack()
    dir_name = os.path.dirname(os.path.realpath(__file__)) + "/static/library"
    notes = piano.getNotes() # get all possible notes C1 to C8
    if (request.method == 'GET'):
        # This code will change as get requests added
        matrix = {}
        fileid = request.args.get("file")
        dirid = request.args.get("dir")
        options = {
            "columns": [0, 0.25, 0.5, 0.75, 1.0, 1.25],
            "notes": map(json.dumps, notes),
            "data": matrix,
            "dirna": dirid,
            "filena": fileid,
            "colors": colors
        }
        return render_template('edit.html', **options)
    else:
        data = request.get_json(silent=True)
        if data is not None: # if form sent from edit.html
            composition = data['container'] # matrix of notes played
            tempo = data['tempo'] #tempo of piece
            length = data['length'] #how many beats in piece

            #parse the composition
            track = piano.get_composition(composition, tempo, length)
            filename = str(data['file'])

            #save composition to library
            piano.saveComposition(filename=filename, track=track)
        dir = "static/library/"
        info = request.form
        files = []
        data = []
        x = []

        #add all selected files from library to matrix
        for v in info:
            files.append(request.form[v])
            results = piano.add_file(filename=dir + v)
            print request.form[v]
            data.append(results[0])
            if len(x) < len(results[1]):
                x = results[1]
        options = {
            "columns": x,
            "notes": notes,
            "data": data,
            "dir": dir_name,
            "files": files,
            "colors": colors
        }

        return render_template('edit.html', **options)

#library
@app.route('/library', methods=['GET', 'POST'])
def library():
    piano.clearTrack()
    dir_name = os.path.dirname(os.path.realpath(__file__)) + "/static/library"
    if request.method =='POST':
        op = str(request.form.get('op'))
        filename = str(request.form.get('filename'))
        if op == "play":
            return redirect(url_for('play'))
        elif op == "edit":
            return redirect(url_for('edit', dir=dir_name, file = filename))
        elif op == "export":
            return send_from_directory(dir_name, filename, as_attachment=True)
        elif op == "discard":
            os.remove(os.path.join(dir_name, filename))
            return redirect(url_for('library'))
        else:
            abort(404)

    else:
        library = os.listdir(dir_name)
        options = {
			"library": library
		}
        return render_template('library.html', **options)

if __name__ == '__main__':
    app.run(debug=True)