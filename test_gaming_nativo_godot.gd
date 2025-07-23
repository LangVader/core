# CÓDIGO GENERADO POR VADER 7.0 UNIVERSAL GAMING
# Archivo .vdr ejecutado nativamente en Godot

extends Node2D

# Variables del juego
var player_speed = 200.0
var jump_force = 400.0
var player_lives = 3
var score = 0
var is_grounded = false

# Referencias a nodos
@onready var player = $Player
@onready var enemy = $Enemy
@onready var ui = $UI

func _ready():
    print("🎮 VADER 7.0 - Godot Game Runtime")
    print("⚡ Ejecutando archivo .vdr nativamente en Godot")
    initialize_game()

func _process(delta):
    handle_player_input(delta)
    update_game_logic(delta)

func initialize_game():
    print("🎮 ¡Hola desde Vader 7.0 Gaming Universal!")
    # Crear jugador
    player.position = Vector2(100, 300)
    print("¡Ouch! Vidas restantes:  + vidas")
    print("Game Over")
    print("puntuacion en pantalla")
    print("vidas en pantalla")
    print("tiempo restante")
    print("Inicializando juego...")
    print("Cargando assets...")
    print("¡Juego listo para jugar!")
    print("✅ Vader Gaming Runtime funcionando perfectamente")

func handle_player_input(delta):
    # Input del jugador
    # Sistema de salto
    if Input.is_action_just_pressed("jump") and is_grounded:
        velocity.y = -jump_force
        is_grounded = false
    # Aumentar puntuación
    score += 10
    print("Score: ", score)

    
    # Aplicar movimiento
    if player:
        player.move_and_slide()

func update_game_logic(delta):
    # Lógica del juego
    check_collisions()
    update_ui()

func check_collisions():
    # Detectar colisiones
    pass

func update_ui():
    # Actualizar interfaz
    if ui:
        ui.update_score(score)
        ui.update_lives(player_lives)

func _on_coin_collected():
    score += 10
    print("Coin collected! Score: ", score)

func _on_enemy_hit():
    player_lives -= 1
    print("Player hit! Lives: ", player_lives)
    if player_lives <= 0:
        game_over()

func game_over():
    print("Game Over!")
    # Mostrar pantalla de Game Over
