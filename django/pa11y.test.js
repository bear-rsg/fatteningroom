/* global test expect describe */

const colourSchemes = ['light', 'dark']

describe('Accessibility tests', () => {

    test('Test all the simple pages with no actions', async () => {
        const urls = [
          "http://127.0.0.1:8000/",
          "http://127.0.0.1:8000/cookies/",
        ];
        for (let i = 0; i < colourSchemes.length; i += 1) {
            await expect(urls).allToBeAccessible(colourSchemes[i]);
        }
    }, 10000 * 4); // increment second number to at least the number of URLs tested * the number of colour schemes

    test('Test the base url with the cookies accepted', async () => {
        const url = "http://127.0.0.1:8000/"
        const newBrowser = true;  // set to true where actions require cookies to be cleared
        const actions = [
            "wait for element #cookie-message-popup-accept to be visible",
            "click element #cookie-message-popup-accept"
        ];
        const waitTime = 1000;
        for (let i = 0; i < colourSchemes.length; i += 1) {
            await expect(url).toBeAccessible(actions, waitTime, colourSchemes[i], newBrowser);
        }
    }, 10000 * 2); // set the second number to the number of colour schemes

});