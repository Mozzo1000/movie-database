async function get_movie(id, apikey) {
    console.log("get_movie")
    var url = new URL("http://www.omdbapi.com/")
    var params = {'i': id, 'plot': 'full', 'apikey': apikey}
    url.search = new URLSearchParams(params).toString()

    const response = await fetch(url);
    const movie = await response.json();

    return movie;
}

async function get_movie_by_title(title, apikey) {
    var url = new URL("http://www.omdbapi.com/");
    var params = {'s': title, 'plot': 'short', 'apikey': apikey}
    url.search = new URLSearchParams(params).toString()

    const response = await fetch(url);
    const movies = await response.json();

    return movies;
}

async function get_movie_from_api(url, endpoint, access) {
    var url = new URL(url + endpoint);
    console.log(access)
    _access = 'Bearer ' + access;

    const response = await fetch(url, {
        mode: 'cors',
        method: 'get',
        headers: new Headers({
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': _access
        })
    });
    const movies = await response.json();

    return movies;
}

Object.prototype.isEmpty = function() {
    for(var key in this) {
        if(this.hasOwnProperty(key))
            return false;
    }
    return true;
}