<template lang="">
  
    <img v-if="movie.poster_path" :src="'https://image.tmdb.org/t/p/w500/'+movie.poster_path"/>
    <img v-else src="/img/poster.jpg"/>

    <h3>{{movie.title || movie.name}}</h3>

    <h5 v-if="movie.release_date || movie.first_air_date">{{dateFormat(movie.release_date || movie.first_air_date)}}</h5>
    <h5 v-else >Fecha no encontrada</h5>

    <Rating :grade="this.stars" :onChange="onRankingChange" :keY="stars"></Rating>

    <ul v-if="movie.genre_ids">
      <li v-for="movieGenre in genresMovies(movie.genre_ids)">
        {{movieGenre}}
      </li>
    </ul>
    <ul v-else>
      <li v-for="genre in movie.genres">
        {{genre.name}}
      </li>
    </ul>

    <h3 v-if="movie.overview">Synopsis</h3>
    <p>{{movie.overview}}</p>
</template>

<script>
import poster from '/img/poster.jpg'
import { CButton } from '@coreui/vue';
import  Rating  from  './Rating.vue';
export default {
  data(){
    return {
      poster: poster, 
    }
  },
  components: {
    CButton,
    Rating
  },
  props: {
    movie: Object,
    genres: Object,
    add: Boolean,
    setDataFromChild:Function,
    
  },
  methods: {
    
    dateFormat(date) {
      let [yy, mm, dd] = date.split('-')
      return [dd, mm, yy].join('/');
    },
    genresMovies(idGenre){
      let genresArray = [];
      for (let i = 0; i < idGenre.length; i++) {
        for (let j = 0; j < this.genres.length; j++) {
          if (idGenre[i] === this.genres[j].id) {
            genresArray.push(this.genres[j].name)
          }
        }
      }
      return genresArray;
    },
    onRankingChange(ranking){
      return this.changeStorage( this.movie, ranking )
    },
    changeStorage(movie, ranking) {
      let storeData = window.localStorage.movies ? window.localStorage.movies.split(',').map(element => {
        let [id, ranking] = element.split(':');
        return {id, ranking};
      }) : [];
     
      storeData = storeData.filter(element => element.id !== movie.id.toString());
      if(ranking != 0)
        storeData.push({id: movie.id, ranking});
      window.localStorage.movies = storeData.map(item => `${item.id}:${item.ranking}`).join(',');
    },
  },
  computed:{
    stars(){
      let storeData = window.localStorage.movies ? window.localStorage.movies.split(',').map(element => {
        let [id, ranking] = element.split(':');
        return {id, ranking};
      }) : [];
      let movie = storeData.find(element => element.id === this.movie.id.toString());
      return movie ? movie.ranking : 0;
    }
  },
  mounted() {
    let storeData = window.localStorage.movies ? window.localStorage.movies.split(',').map(element => {
      let [id, ranking] = element.split(':');
      return {id, ranking};
    }) : [];
  }
}
</script>
