<p align="center">
  <img src="https://github.com/user-attachments/assets/25ee94f6-ac12-4134-b5b0-540600ea28f3" alt="Directorybrute" width="400">
</p>
## Description:

**HackerlabsCtfs Tool** is a command line tool designed to interact with the HackerLabs page. It allows you to extract and display information about CTF (Capture The Flag) machines available on the HackerLabs platform. You can filter machines by difficulty, search by creator, get a random machine, and more.

## Install:

To install and configure the tool, follow these steps:

### **Clone the repository:**

```bash
git clone https://github.com/D1se0/hackerlabsCtfs-tool.git
cd HackerlabsCtfs
```

## Prepare the environment and dependencies:

Run the requirements.sh script as root to install the dependencies and configure the symbolic link:

```bash
sudo ./requirements.sh
```

Make sure you have the requirements.txt file in the same directory as the requirements.sh script. This file should contain all necessary dependencies.

## Use:

Once the tool is installed, you can use it from the command line. Below are some practical examples on how to use the tool.

### Show Banner:

To see the welcome banner and basic tool information, run:

```bash
python3 hackerlabsCtfs
```

### Filter by Difficulty:

To list machines of a specific difficulty, use the `-d` parameter. The difficulty levels available are:

'Very Easy'

'Easy'

`Medium`

'Difficult'

### Example to filter machines of "Medium" difficulty:

```bash
python3 hackerlabsCtfs -d medio
```

### Search by Creator:

To filter machines created by a specific creator, use the `-c` parameter:

```bash
python3 hackerlabsCtfs -c d1se0
```

### Get a Random Machine:

To get a random machine among those available, use the `-a` parameter:

```bash
python3 hackerlabsCtfs -a
```

### Show Machine Information by Name:

To search and display information about a specific machine by name, use the `-n` parameter:

```bash
python3 hackerlabsCtfs -n vulnvault
```

### Mark a Machine as Completed:

To mark a machine as finished, use the `-f` parameter followed by the machine name:

```bash
python3 hackerlabsCtfs -f vulnvault
```

### List Machines Marked as Completed:

To list all the machines you have marked as finished, use the `-l` parameter:

```bash
python3 hackerlabsCtfs -l
```

### Disable Colors:

If you prefer to disable colors in the output, use the `--no-colores` parameter:

```bash 
python3 hackerlabsCtfs --no-colores
```

## Technical Details:

The tool extracts information from the HackerLabs page using `BeautifulSoup` for HTML analysis and requests for downloading web content. Information about CTF machines is displayed on the command line with colors for easy viewing.

## Contribute:

If you want to contribute to the development of this tool, please open an issue or send a pull request with your improvements or corrections.

## License:

This project is licensed under the MIT License. See the LICENSE file for more details.

For more information, visit our website: [http://hackerlabs.com/](LINK_PAGINA) or learn more in [HackerLabs Hacking Guide](LINK_PAGINA_GUIA_HACKING).
