class SearchBox {
    constructor() {
        this.args = {
            searchBox: document.querySelector('.search_support'),
            sendButton: document.querySelector('.search__button')
        }
        this.username = ''
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
        this.username  = text1
        if (text1 === "") {
            return;
        }

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
        var html = '<div class="result_boby">'
        alert('done')
        var image_url = '<img class="img_profile" src="static/images/output/'+ this.username +'_propic.jpg"/>';
        html += '<div class="img_view">'+ image_url + '</div>';
        html += '<div class="Name"> <h3> ' + this.result.full_name + '</h3> </div>';
        html += '<div class="follower">FOLLOWER :' + this.result.edge_followed_by + '</div>';
        html += '<div class="follower">FOLLOWING :' + this.result.edge_follow + '</div>';

        html += '<div class="biography"> BIO' + this.result.biography + '</div>';
        html += '</div>'
        const searchboxresult = searchBox.querySelector('.search__result');

        searchboxresult.innerHTML = html;
    }


}
const searchbox = new SearchBox();
searchbox.display();