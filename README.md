# The Tail of the Copy Cat

A clipboard history manager for ubuntu ( not sure about other distros ) using xclip. 
It stores the history of copied items and shows them in a neat gui with keyboard controls to easily switch between them.

## Installation steps
clone the repository and change the current working directory to the same
```bash
cd <desired-directory-to-store-the-code>
git clone https://github.com/imdaredevil/copy-cat-tail
cd copy-cat-tail
```
make the installation script executable and execute it
```bash
chmod +x install
./install
```

## Run manually
In a new tab, run the following command
```bash
copy-cat-tail-server
```

This will start the server which can listen to copied items and store them.
While the above process is running, in a separate tab, run the following

```bash
copy-cat-tail-show
```
A popup showing the last copied item will be shown. We can switch between previous ones by clicking the arrows above. or pressing Ctrl + Left/Right arrow keys. As soon as you release the Ctrl key, the popup will close. The text that you chose must be in the current clipboard and when you click paste / Ctrl + v (or Ctrl + Shift + V in terminal), the text would appear.

## Post Installation steps

We can add a keyboard shortcut ( with Ctrl since navigation buttons use Ctrl) for ``copy-cat-tail-show`` and add ``copy-cat-tail-server`` to startup-applications using gnome-session



