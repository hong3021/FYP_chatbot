class SearchBox {
    constructor() {
        this.args = {
            searchBox: document.querySelector('.search_support'),
            sendButton: document.querySelector('.search__button')
        }
        this.result = [];
    }

    display() {
        const {searchBox, sendButton} = this.args;
        sendButton.addEventListener('click', () => this.onSendButton(searchBox))
        node.addEventListener("keyup", ({key}) => {
            if (key === "Enter") {
                this.onSendButton(searchBox)
            }
        })
    }
    onSendButton(searchBox) {

        var textField = searchBox.querySelector('input');
        let text1 = textField.value
        if (text1 === "") {
            return;
        }
        await delay(5000);
        fetch('http://127.0.0.1:5000/search', {
            method: 'POST',
            body: JSON.stringify({ username: text1 }),
            mode: 'cors',
            headers: {
              'Content-Type': 'application/json'
            },
          })
          .then(r => r.json())
          .then(r => {
            this.result = r
            this.updateSearchText(searchBox)
            textField.value = ''

        }).catch((error) => {
            console.error('Error:', error);
            this.updateSearchText(searchBox)
            textField.value = ''
          });

    }

    updateSearchText(searchBox) {
        var html = ''
        html += '<div>' + this.result.full_name + '</div>';


        const searchboxresult = searchBox.querySelector('.search__result');

        searchboxresult.innerHTML = html;
    }


}
const searchbox = new SearchBox();
searchbox.display();