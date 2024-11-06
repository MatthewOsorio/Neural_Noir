using UnityEngine;
using UnityEngine.SceneManagement;  //Required for SceneManager functions

//Script for menus
//Scene 0 = Main Game, Scene 1 = Main Menu, Scene 2 = Settings, more will be added later.
//Find the scene index values by clicking file>>build profile>>scene list. Must open to edit.
//Please only reorder scenes if absolutely necessary!
public class MenuScript : MonoBehaviour
{
    public KeyCode backButton = KeyCode.Escape; //Designates esc as the back button
    public int currentScene;

    private void Start()
    {
        //empty right now but I'm leaving it for later if we need it.
    }

    private void Update()
    {
        currentScene = SceneManager.GetActiveScene().buildIndex;

        //Used to navigate back from a submenu.
        //When esc is pressed, it will take you to the previous menu screen as long as the current menu
        //is not the main menu (scene index 1). 
        if (Input.GetKeyDown(backButton)&&currentScene>1)
        {
            LoadPreviousMenu();
        }
    }
    public void GameStart()
    {
        SceneManager.LoadScene(0);
    }

    public void LoadSettings()
    {
        SceneManager.LoadScene(2);
    }

    public void GameQuit()
    {
        Debug.Log("Application closed.");
        Application.Quit();
    }

    public void LoadPreviousMenu()
    {
        SceneManager.LoadScene(currentScene - 1);
    }
}
