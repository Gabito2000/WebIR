<template>
  <div class="rating">
    <ul class="list">
      <li :key="star" v-for="star in maxStars" :class="{ 'active': star <= stars }" @click="rate(star)" class="star">
        ★
      </li>
    </ul>
    <ul>
      <li v-if="stars">
        <!-- <button @click="rate(0)" shape="rounded-pill" :class="reset" >Reset</button> -->
        <!-- replace the button with a span -->
        <span @click="rate(0)" shape="rounded-pill" class="reset" >Reset</span>
      </li>
    </ul>
    <span v-if="hasCounter">{{ stars }} of {{ maxStars }}</span>
  </div>
</template>

<script>
  export default {
    name: "Rating",
    props: {
      onChange: {
        type: Function,
        default: () => {}
      },
      grade: {
        type: Number,
        required: true
      },
      maxStars: {
        type: Number,
        default: 5
      },
      hasCounter: {
        type: Boolean,
        default: true
      }
    },
    data() {
      return {
        stars: 0
      }
    },
    methods: {
      rate(star) {
        if (
          typeof star === 'number' &&
          star <= this.maxStars &&
          star >= 0
        )
          this.stars = this.stars === star ? star - 1 : star
          this.onChange(this.stars)
      }
    },
    mounted(){
      console.log({grade:this.grade})
      this.stars = this.grade
    }
  }
</script>

<style scoped lang="scss">
  $active-color: #f3d23e;

  .rating {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    font-size: 22px;
    color: #a7a8a8;
  }
  .list {
    margin: 0 0 5px 0;
    padding: 0;
    list-style-type: none;
    &:hover {
      .star {
        color: $active-color;
      }
    }
  }
  .star {
    display: inline-block;
    cursor: pointer;
    &:hover {
      &~.star {
        &:not(.active) {
          color: inherit;
        }
      }
    }
  }
  //makes the span on hover the same color as the stars when they are active (yellow) and makes it ocupy all the row
  //
  .reset{
    display: inline-block;
    width: 100%;
    cursor: pointer;
    &:hover {
      color: $active-color;
    }
  }
  .active {
    color: $active-color;
  }
  // all with
</style>
