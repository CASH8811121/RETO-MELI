from flask import Flask, render_template, request, redirect, url_for, Response, jsonify, session
from decouple import config
import random
import requests

#PRUEBA OAUTH
from authlib.integrations.flask_client import OAuth

app=Flask(__name__)

#PRUEBA OAUTH
app.secret_key=config('LLAVE_SECRETA_APP')

oauth = OAuth(app)
gooogle = oauth.register(
    name='google',
    client_id=config('CLIENTE_ID'),
    client_secret=config('CLIENTE_SECRETO'),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope' : 'email'},
)
  
#Pagina index
@app.route('/')
def indice():
    email = dict(session).get('email', None) 
    return render_template('index.html',email=email)

 # ruta para login
 
@app.route('/login')
def login():
    google = oauth.create_client('google')
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

 # ruta para autorizacion

@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    resp.raise_for_status()
    user_info = resp.json()
    session['email'] = user_info ['email']
    
    # lo va a redireccionar a la principal
    return redirect('/')


 # ruta para logout

@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
        # lo va a redireccionar a la principal
    return redirect('/')

 
 


################# rutas challengue pokemon ################# 

#Obetener el tipo de Pokemon por su nombre

@app.route('/tipo', methods=['GET', 'POST'])
def obtener_tipo_pokemon():
    if request.method == 'POST':
        # sacar el nombre del Pokémon ingresado por el usuario en el formulario
        nombre_pokemon = request.form['nombre_pokemon']
        
        # consulta a Poké API para obtener los datos del Pokémon por nombre
        response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{nombre_pokemon.lower()}')
        
        if response.status_code == 200:
            pokemon = response.json()
            tipo = pokemon['types'][0]['type']['name']
            return jsonify({'nombre': nombre_pokemon, 'tipo': tipo})
        else:
            return jsonify({'error': 'Pokémon no encontrado'}), 404

    return '''
        <form method="post">
            <label for="nombre_pokemon">Nombre del Pokémon:</label>
            <input type="text" id="nombre_pokemon" name="nombre_pokemon">
            <input type="submit" value="Consultar">
        </form>
    '''











#Obetener el tipo de Pokemon al azar por su tipo

@app.route('/azar', methods=['GET', 'POST'])
def obtener_pokemon_al_azar():
    if request.method == 'POST':
        # Sacar el tipo de Pokémon seleccionado por el usuario en el formulario
        tipo_pokemon = request.form['tipo_pokemon']
        
        # Hacer una consulta a Poké API para obtener la lista de Pokémon de un tipo específico
        response = requests.get(f'https://pokeapi.co/api/v2/type/{tipo_pokemon.lower()}')
        
        if response.status_code == 200:
            tipo = response.json()
            pokemon = random.choice(tipo['pokemon'])
            nombre_pokemon = pokemon['pokemon']['name']
            return jsonify({'nombre': nombre_pokemon, 'tipo': tipo_pokemon})
        else:
            return jsonify({'error': 'Tipo de Pokémon no encontrado'}), 404

    return '''
        <form method="post">
            <label for="tipo_pokemon">Tipo de Pokémon:</label>
            <input type="text" id="tipo_pokemon" name="tipo_pokemon">
            <input type="submit" value="Consultar">
        </form>
    '''

#Obetener el nombre mas largo del Pokemon por su tipo

@app.route('/largo', methods=['GET', 'POST'])
def obtener_pokemon_nombre_mas_largo():
    if request.method == 'POST':
        # Obtener el tipo de Pokémon seleccionado por el usuario en el formulario
        tipo_pokemon = request.form['tipo_pokemon']
        
        # Hacer una consulta a Poké API para obtener la lista de Pokémon de un tipo específico
        response = requests.get(f'https://pokeapi.co/api/v2/type/{tipo_pokemon.lower()}')
        
        if response.status_code == 200:
            tipo = response.json()
            pokemon_mas_largo = None
            longitud_maxima = 0
            
            # Recorrer la lista de Pokémon del tipo específico y encontrar el nombre más largo
            for pokemon in tipo['pokemon']:
                nombre_pokemon = pokemon['pokemon']['name']
                longitud_nombre = len(nombre_pokemon)
                if longitud_nombre > longitud_maxima:
                    longitud_maxima = longitud_nombre
                    pokemon_mas_largo = nombre_pokemon
                    
            return jsonify({'nombre': pokemon_mas_largo, 'tipo': tipo_pokemon})
        else:
            return jsonify({'error': 'Tipo de Pokémon no encontrado'}), 404

    return '''
        <form method="post">
            <label for="tipo_pokemon">Tipo de Pokémon:</label>
            <input type="text" id="tipo_pokemon" name="tipo_pokemon">
            <input type="submit" value="Consultar">
        </form>
    '''



  
if __name__=='__main__':
    app.run(debug=True, port=5000)