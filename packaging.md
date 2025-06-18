# Packaging Instructions (so I don't forget)

## instructions for windows (how to package):
This project uses maven as a project/build manager. In order to build the project into an executable .jar, you will need to install maven. For windows, there are a couple options:
* **Chocolatey**: If you have chocolatey installed, run `choco install maven`
* **WSL**: If you have windows subsystem for linux, run `sudo apt install maven`.
    * if you choose this option, all the packaging commands must be run from a wsl terminal
* **Install from zip:** If none of these options work, you can also install maven from the [maven download page](https://maven.apache.org/download.cgi), and extract it to a directory of your choice (normally C:\Program Files\...). Then, add it to your environment variables (follow [this tutorial](https://phoenixnap.com/kb/install-maven-windows) if you need help)

Now, check that you have maven installed by opening a terminal and running `mvn --version`.

There are two options that I tested when trying to package the GUI for windows: Launch4J and Packr. Launch4J has its own interface which makes it much easier to use, but it requires an extra download. Packr runs from the command line and is relatively easy to use, but if the configs for it which are defined in `packr-configs_*.json` are not correct, it will not work properly.

---
### Using Packr:
For the purposes of this project, Packr has already been downloaded and the .jar for it is located in the `/packr` directory. If packer is not downloaded, you can download it [here](https://github.com/libgdx/packr/releases), and you can also view the [documentation](https://github.com/libgdx/packr) for it explains how to write a .json configs file to make it run properly. This should all be set up already.

1) First, package the project as a .jar file using maven:
    * ```mvn clean package```


2) run the command:
    * ```java -jar packr/packr-all-4.0.0.jar packr/packr-config_win.json```
    * packr decides where to put things based on what is defined in the `packr-configs_*.json` file. make sure you are using the correct `.json` file for your operating system
    * You can update the location of which the .exe will be in `packr-configs_*.json` by modifying the `"output"` field on line 18


3) Verify that the .exe works by `cd` into the output directory and running `MPR-Bio-Remote.exe`, or opening a file explorer, navigating to the output directory and clicking on the .exe
    * If the .exe does not work, there is likely something wrong with the configs file or the JRE.

### Using Launch4J:
Launch4J is a good tool if you are packaging a .jar into a .exe for the first time, but I recommend using packr for this project if you need to create a .exe again. Launch4J has a user interface which makes it easier to tell what is doing what the first time around. Here is the [documentation](https://launch4j.sourceforge.net/docs.html) for Launch4J.
1) First, package the project as a .jar file using maven:
   ```mvn clean package```


2) Download [Launch4J](https://sourceforge.net/projects/launch4j/files/launch4j-3/3.50/) and open it


3) Configuring File Paths:
    * **Output File** &rarr; the location where you want the .exe to be.
        * The jre-win, python, and python-scripts folders bust be copied/moved into the output location.
    * **Jar** &rarr; the file path to the .jar that you created in [step 1]
    * Optional:
        * **Icon** the location where a .ico icon is located


4) Navigate to Classpath tab to set the Classpath
    * check **Custom Classpath**
    * **Main Class** &rarr; `GUI.BuildGUI`


5) Configure the Java Runtime Environment (JRE) in the JRE Tab
    * I already downloaded in the JRE for windows in the jre-win folder which should be copied into the output folder.
    * **JRE Paths** &rarr; jre-win


6) Save and compile
    * saving will create a .xml log file in a location of your choice
    * after saving hit the gear button and your .exe should be created
---
For windows, if you just package using Launch4J or Packr, the .exe file must be placed in a specific folder or else it won't work (the GUI will not know where to find the python backend and bundled python). To get around this, I used a program called **[inno setup compiler](https://jrsoftware.org/isdl.php)**, to make it look like everything is running from a single .exe file. The way that it works is it prompts the user to choose a location to download the MPR-Bio-Remote project which contains the .exe that we built using packr/Launch4J and all the necessary resources,then creates a separate .exe that points to the original .exe at that location. So in other words, **it creates a shortcut that just points to the actual location of the project**.

If you want to use inno setup compiler, simply download it at the link above, then run the script in `setup\installer.iss`. To do this:
1) open inno setup app, copy and paste the 'installer.iss' script into the editor
2) hit save (make sure you change the file path to the correct location where the MPR-Bio-Remote project is located).
3) hit the compile button which should be located right next to the save button. If you can't find it, you can also run the command using `Ctrl+F9`. Compiling the script will create an output file in the root folder where your project is located.
4) If you run `./Output/setup`, you will be prompted to download the project to a location of your choice. finishing this setup will create the shortcut which it will feel just like you are running a single .exe file that can be located anywhere.

For distribution, we can either use the setup guy created from inno setup compiler, or just distribute the original .exe along with the necessary packages and give instructions on how to set up the project structure. I think the setup guy is easier, but it does require one extra step on our end.

---

---

## instructions for mac (how to package):
Packaging on mac has a few extra steps because I didn't want to set up github on my girlfriend's computer.
### Installing maven
First of all, make sure maven is installed on your system. if you have hombrew, you can run the command `brew install maven` or follow the instruction in [this tutorial](https://www.digitalocean.com/community/tutorials/install-maven-mac-os). Verify that you have maven on your computer by running `mvn --version`. You will also need to download and extract a JRE for mac to the `./jre-mac` folder:
1) Go to [adoptium temurin](https://adoptium.net/temurin/releases/?os=any&arch=any&version=21) and find the correct download for your system
2) Make sure to select JRE from the dropdown, not JDK.
3) Extract the .tar or .pkg, and move all the files into the `./jre-mac` directory already created in this repository. (alternatively, rename the extracted folder jre-mac and replace the one in this repo with that one).
   Finally, I tried to figure out a way to embed python into the mac .app file, but I just could not figure out how because macbooks apparently come preinstalled with python? make sure you have python installed on your system and that it is at least python 3.10 (the backend uses match case statements which won't work for older versions of python. If that is all set, you can now actually package the app using packr:

### Using packr
1) First, package the project as a .jar file using maven:
    * ```mvn clean package```


2) run the command:
    * ```java -jar packr/packr-all-4.0.0.jar packr/packr-config_mac.json```
    * packr decides where to put things based on what is defined in the `packr-configs_*.json` file. make sure you are using the correct `.json` file for your operating system
    * You can update the location of which the .app will be in `packr-configs_*.json` by modifying the `"output"` field on line 18, but make sure not to change `"./MPR-Bio-Remote.app"` at the end because I found that it breaks everything.

3) Run `MPR-Bio-Remote.app` by navigating to the output directory and double-clicking on it

I wasn't able to do that much testing for the app on mac, and I am a bit skeptical that everything is actually included in the .app because where do the resources even go? are they contained inside the .app? Also, the SetupWizard creates a host_config.properties file which contains the file path to where profiles are stored and where data will be synced to but i don't know where that ends upp with the mac app because in windows it just goes into the project directory... Anyways, I am hoping that as long as your python is up-to-date it works as it should.