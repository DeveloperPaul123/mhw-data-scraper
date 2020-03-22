# mhw-data-scraper
A collection of web-scraper scripts for getting MHW data from various wikis/websites.

This is a *very* work in progress project. The main goal of this project is to be able to pull data from Kiranico and other sources/wikis/websites that are not yet available elsewhere for the Iceborne expansion of MHW. 

## Requirements

To run the script you will need:

* Python 3 (tested with `3.8+`)
* Python packages (install with pip if missing)
  * `requests`: HTML requests
  * `requests-html`: Headless browser html requests with the ability to load dynamic content
    * Note that you may need to force install `websockets` version `6.0` due to a pyppeteer [issue](https://github.com/miyakogi/pyppeteer/issues/171#issuecomment-478338932)
  * `re`: Regular expressions
  * `bs4`: BeautifulSoup html parser/scraper
  * `urllib`
  * `csv`: CSV file output/input

## Usage

The project includes a number of scrapers that can be used to collect MHW data. Each `.py` file in the project is meant to be run as a stand alone scraper script. Simply open the script you want to use and run it!

## Related Projects

This project is inspired/motivated by other similar projects, most notably the [MHWorldData](https://github.com/gatheringhallstudios/MHWorldData) project. Other projects include:
* [MHW DB API](https://github.com/LartTyler/MHWDB-Docs/wiki)

## License

This project is licensed under the MIT license. See [LICENSE](LICENSE) for more details.

## Author

| [<img src="https://avatars0.githubusercontent.com/u/6591180?s=460&v=4" width="100"><br><sub>@DeveloperPaul123</sub>](https://github.com/DeveloperPaul123) |
|:----:|