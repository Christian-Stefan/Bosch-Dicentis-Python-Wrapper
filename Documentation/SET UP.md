### Wrapper setup in a few words...

> [!NOTE]
> Note that the hyperlinks attached to the upcoming enumerated elements might become outdated.
> For [Word 1](#word-1----infrastructure-dependencies) reach out to *fixed-term.Stefan.Gheorghiu@keenfinity-group.com*.
> For [Word 2](#word-2----python-dependencies), Meeting Application section contact *fixed-term.Stefan.Gheorghiu@keenfinity-group.com*. For any other item in the same section, get in touch with their associated support.

## Word 1 🔗 - *Infrastructure dependencies*
- Confrence Wired System which includes at least an [APS2](https://commerce.keenfinity.tech/nordics/en/Audio-processor-and-powering-switch/p/F.01U.308.936), [Server 3](https://commerce.keenfinity.tech/nordics/en/System-server/p/F.01U.404.927) and any [Dicentis Discussion Device](https://commerce.keenfinity.tech/nordics/en/Discussion-device/p/F.01U.313.726);
- Any IDE (e.g, [Visual Studio](https://code.visualstudio.com), [PyCharm](https://www.jetbrains.com/de-de/pycharm/#))

## Word 2 🐍 - *Python dependencies*
- [IronPython](https://github.com/IronLanguages/ironpython3/releases/tag/v3.4.2), choosing the variant that suits to your machine needs (e.g., Windows ~ IronPython.3.4.2.zip);
- Python related dependencies are to be found in requirements.txt;
- [Meeting Application](https://software-download.keenfinity-group.com/conference/default.aspx);

## Word 3 🧩 - *Put the dependencies together*
- ### 1. Donwload and install all the aforementioned dependencies;
- ### 2. Set up the Meeting Application as shown [here](https://www.youtube.com/watch?v=YcliO_5UrHk);
- ### 3. Create an empty project in your IDE where the cloned project must be placed;
Write in your project's terminal the following git command:

```
git clone https://github.com/Christian-Stefan/Bosch-Dicentis-Python-Wrapper.git

``` 
- ### 4. Install  requirements.txt
```
pip install -r /path/to/requirements.txt
```
- ### 5. Fill in `dependencies.py` with required hard coded information (e.g., the generic path of Bosch App .DLLs - C:\Program Files\Bosch\DICENTIS)
```
# ---- Hard Coded Paths ----
path = "C:\Program Files\Bosch\DICENTIS"
# ---- End of Hard Coded Paths ---
```
