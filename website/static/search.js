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
        alert('IT MAKE TAKE TIME TO SEARCH')
        var textField = searchBox.querySelector('.user__input');
        let text1 = textField.value
        var address = searchBox.querySelector('.chack__address');
        let address_status = address.checked;
        this.username  = text1
        if (text1 === "") {
            return;
        }

        fetch('http://127.0.0.1:5000/search', {
            method: 'POST',
            body: JSON.stringify({ username: text1, find_address: address_status }),
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
        var image_url = '<img class="img_profile" src="static/images/output/'+ this.username +'_propic.jpg"/>';
        html += '<div class="img_view">'+ image_url + '</div>';
        html += '<div class="Name"> <h3> ' + this.result.full_name + '<a href="https://www.instagram.com/'+ this.username + '" target="_blank"> [' + this.username +']</a></h3> </div>';
        html += '<div class="follower">FOLLOWER :' + this.result.edge_followed_by + '</div>';
        html += '<div class="follower">FOLLOWING :' + this.result.edge_follow + '</div>';

        html += '<div class="biography"> BIO :' + this.result.biography + '</div>';
        if (this.result.address){
            html += '<div class="address_title"><h3> Leatest Address </h3></div>';
            for (let i in this.result.address){
                html += '<div class="address">'+ i + ". " + this.result.address[i].address + ' -['+ this.result.address[i].time + ']</div>';
            }
        }
        html += '</div>'
        const searchboxresult = searchBox.querySelector('.search__result');

        searchboxresult.innerHTML = html;
    }


}
const searchbox = new SearchBox();
searchbox.display();