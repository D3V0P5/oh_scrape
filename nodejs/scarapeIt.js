"use strict;"
const request = require('request');
const cheerio = require('cheerio');
//Thogh not used it's nice to have. espacially with non English fonts:
const jsesc = require('jsesc') ;
const camo = require('camo') ;
const Document = camo.Document ;
const EmbeddedDocument = camo.EmbeddedDocument ;



class Fact extends EmbeddedDocument {
  constructor() {
    super();
    this.content = {
      type : String ,
    };
  }
}

class Song extends EmbeddedDocument {
  constructor() {
    super();
    this.name = {
      type : String ,
    };
    this.facts = [Fact] ;

  }
}

class Artist extends Document {
  constructor(){
    super();
    this.name = {
      type : String ,
      unique: true ,
    } ;
    this.songs = [Song] ;
  }
}

//Format: mongodb://[username:password@]host[:port][/db-name]
camo.connect( 'mongodb://172.17.0.2/mima').then(function(db) {
    // Ready to use Camo!
    //(documantation says so)
});

for (let i = 1 ; i < 1500 ; i++){
  request(`http://localhost/facts/page.php?song_id=${i}`,
    function (error, response, html) {
      if (!error && response.statusCode == 200) {
        let $ = cheerio.load(html) ;
        const artist = $('font[size="+2"]').text() ;
        let mArtist = Artist.create() ;
        mArtist.name = artist ;
        const song = $('font[size="+5"]').text() ;
        let mSong = Song.create() ;
        mSong.name = song ;
        mArtist.songs.push(mSong) ;
//$('table[width="60%"]').. ...text() Yealds to a single string so we need to brake it
      $('table[width="60%"]').children('tr').children('td').each(function(i, elem) {
        const fact = $(this).text() ;
        mFact = Fact.create() ;
        mFact.content = fact ;

        mSong.facts.push(mFact) ;
      });

      mArtist.save().then(function(l) {
          console.log(`Added Artist ${l}. YEEI`);
          });
    }
  });
}
