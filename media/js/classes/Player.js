function Player() {
    this.isiPad = navigator.userAgent.match(/iPad/i) != null;
    this.last_fm_id = "9530d1e6f1d1b81032f024e99d8771b9";
    
    try {
        this.storage = window.localStorage || window.globalStorage[document.domain];
    } catch(e) {
        this.storage = {};
    }

    soundManager.url = '/swf/';
    soundManager.debugMode = false;
    soundManager.flashVersion = 9; // optional: shiny features (default = 8)
    soundManager.useFlashBlock = true; // optionally, enable when you're ready to dive in
    soundManager.useHTML5Audio = true; // enable HTML5 audio support, if you're feeling adventurous.
    soundManager.useHighPerformance = true;

    soundManager.onready(function() {
        if (!soundManager.supported()) {
            gui.showUnsupported();
        }
    });

    this.eventListeners = {};

    this.listController = new ListController(this);
    this.playbackController = new PlaybackController(this);
    this.searchController = new SearchController(this);
    this.scrobblerController = new ScrobblerController(this);

    this.eventListeners = {
        "TrackPlay": [ this.listController, this.scrobblerController ],
        "TrackJustBeforeFinish": [ this.scrobblerController ],
        "NoSidebarInfo": [ this.searchController ],
        "Search": []
    };
    //this.fireEvent("NoSidebarInfo");
}

Player.prototype.addEventListener = function(event, listener) {
    if (!this.eventListeners[event]) {
        this.eventListeners[event] = [];
    }
    this.eventListeners[event].push(listener);
};

Player.prototype.removeEventListener = function(event, listener) {
      this.eventListeners[event].splice(this.eventListeners[event].indexOf(listener), 1);
};

Player.prototype.fireEvent = function(event) {
    if (this.eventListeners[event]) {
        for(var i = 0; i < this.eventListeners[event].length; i++) {
            this.eventListeners[event][i].handleEvent(event);
        }
    }
};

Player.prototype.tweetNowPlaying = function() {
    var track = this.playbackController.current_track;
    if (!track) {
        alert("First you need to listen to something");
        return;
    }
    window.open("https://twitter.com/intent/tweet?related=player_vas3k_ru&text=Слушаю%20сейчас:%20" + track.artist + "%20—%20" + track.title + "%20http://player.vas3k.ru/small/track/" + track.id + "%20@player_vas3k_ru",
                "Tweet track",
                'top=300, left=200, menubar=0, toolbar=0, location=0, ' +
                'directories=0, status=0, scrollbars=0, resizable=1, width=600, height=300');
};

Player.toggleVk = function() {
    player.searchController.activate('vk');
    return false;
};

Player.toggleLastfm = function() {
    window.open('http://www.last.fm/api/auth?api_key=9530d1e6f1d1b81032f024e99d8771b9',
        'Last.fm login',
        'width=800,height=600,resizable=yes,scrollbars=yes,status=no');
    return false;
};
