<template>
  <router-view></router-view>
</template>

<style>
body {
  font-family: Arial, Helvetica, sans-serif;
  font-size: .875rem;
  background-color: #f8f9fa;
}
.container {
  max-width: 900px;
}
.feather {
  width: 16px;
  height: 16px;
  vertical-align: text-bottom;
}
.bd-placeholder-img {
    font-size: 1.125rem;
    text-anchor: middle;
    -webkit-user-select: none;
    -moz-user-select: none;
    user-select: none;
}

@media (min-width: 768px) {
    .bd-placeholder-img-lg {
      font-size: 3.5rem;
    }
}
.sidebar .collapsed {
  width: 70px;
}
.multiselect-options {
    display: flex;
    flex-direction: column;
    list-style: none;
    margin: 0;
    padding: 0;
    color: #212529;
}
</style>
