<template >
    <div class="background-radial-gradient text-white min-vh-100">
        <h1>404</h1>
        <p>Oops! Something is wrong.</p>
        <RouterLink :to="{ name: 'Home' }" class="button">
            Go back in initial page, is better. </RouterLink>

    </div>
</template>   

<style scoped>
p {
    text-align: center;
}

h1 {
    text-align: center;
    font-size: 15em;
    font-weight: 100;
}

.background-radial-gradient {
    background-color: hsl(218, 41%, 15%);
    background-image: radial-gradient(650px circle at 0% 0%,
            hsl(218, 41%, 35%) 15%,
            hsl(218, 41%, 30%) 35%,
            hsl(218, 41%, 20%) 75%,
            hsl(218, 41%, 19%) 80%,
            transparent 100%),
        radial-gradient(1250px circle at 100% 100%,
            hsl(218, 41%, 45%) 15%,
            hsl(218, 41%, 30%) 35%,
            hsl(218, 41%, 20%) 75%,
            hsl(218, 41%, 19%) 80%,
            transparent 100%);
}

.button {
    font-weight: 300;
    color: #fff;
    font-size: 1.2em;
    text-decoration: none;
    border: 1px solid #efefef;
    padding: .5em;
    border-radius: 3px;
    float: left;
    margin: 6em 0 0 -155px;
    left: 50%;
    position: relative;
    transition: all .3s linear;
}

.button:hover {
    background-color: #007aff;
    color: #fff;
}
</style>

<script>
export default {
    name: "NotFound"
}
</script>