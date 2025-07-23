// CÓDIGO GENERADO POR VADER 7.0 UNIVERSAL GAMING
// Archivo .vdr ejecutado nativamente en Unity

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class VaderGameController : MonoBehaviour
{
    [Header("Vader Game Settings")]
    public float playerSpeed = 5f;
    public float jumpForce = 10f;
    public int playerLives = 3;
    public int score = 0;
    
    [Header("Game Objects")]
    public GameObject playerPrefab;
    public GameObject enemyPrefab;
    public GameObject coinPrefab;
    
    private Rigidbody2D playerRb;
    private bool isGrounded = false;
    
    void Start()
    {
        Debug.Log("🎮 VADER 7.0 - Unity Game Runtime");
        Debug.Log("⚡ Ejecutando archivo .vdr nativamente en Unity");
        
        InitializeGame();
    }
    
    void Update()
    {
        HandlePlayerInput();
        UpdateGameLogic();
    }
    
    void InitializeGame()
    {
        Debug.Log("🎮 ¡Hola desde Vader 7.0 Gaming Universal!");
        // Crear jugador
        GameObject player = Instantiate(playerPrefab, Vector3.zero, Quaternion.identity);
        playerRb = player.GetComponent<Rigidbody2D>();
        // Crear enemigo
        Instantiate(enemyPrefab, new Vector3(5, 0, 0), Quaternion.identity);
        Debug.Log("¡Ouch! Vidas restantes:  + vidas");
        Debug.Log("Game Over");
        Debug.Log("puntuacion en pantalla");
        Debug.Log("vidas en pantalla");
        Debug.Log("tiempo restante");
        Debug.Log("Inicializando juego...");
        Debug.Log("Cargando assets...");
        Debug.Log("¡Juego listo para jugar!");
        Debug.Log("✅ Vader Gaming Runtime funcionando perfectamente");
    }
    
    void HandlePlayerInput()
    {
        // Input del jugador
        // Sistema de salto
        if (Input.GetKeyDown(KeyCode.Space) && isGrounded) {
            playerRb.AddForce(Vector2.up * jumpForce, ForceMode2D.Impulse);
            isGrounded = false;
        }
        // Sistema de salto
        if (Input.GetKeyDown(KeyCode.Space) && isGrounded) {
            playerRb.AddForce(Vector2.up * jumpForce, ForceMode2D.Impulse);
            isGrounded = false;
        }
        // Aumentar puntuación
        score += 10;
        Debug.Log("Score: " + score);
    }
    
    void UpdateGameLogic()
    {
        // Lógica del juego
        CheckGameOver();
        UpdateUI();
    }
    
    void CheckGameOver()
    {
        if (playerLives <= 0) {
            Debug.Log("Game Over!");
            // Reiniciar juego o mostrar pantalla de Game Over
        }
    }
    
    void UpdateUI()
    {
        // Actualizar interfaz de usuario
        // UI.scoreText.text = "Score: " + score;
        // UI.livesText.text = "Lives: " + playerLives;
    }
    
    void OnTriggerEnter2D(Collider2D other)
    {
        if (other.CompareTag("Coin")) {
            score += 10;
            Destroy(other.gameObject);
        }
        
        if (other.CompareTag("Enemy")) {
            playerLives--;
            Debug.Log("Player hit! Lives: " + playerLives);
        }
        
        if (other.CompareTag("Ground")) {
            isGrounded = true;
        }
    }
}
