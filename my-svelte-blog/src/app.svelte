<script>
	import Blog from "./routes/blog/+blog.svelte";
	import About from "./routes/about/+about.svelte";
	import LandingPage from "./landing-page.svelte";
	import { onMount } from "svelte";
	let currentPage;

	onMount(() => {
		currentPage = window.location.pathname;
		debugger
	});
</script>

<section class="navbar-content">
	{#if currentPage === "/"}
		<LandingPage />
	{:else if currentPage === "/blog"}
		<Blog />
	{:else if currentPage === "/about"}
		<About />
	{/if}
</section>

<!-- <LandingPage /> -->
<nav class="navbar">
    <a class="navbar-item" href="blog">Blog</a>
    <a class="navbar-item" href="about">About</a>
</nav>

<style>
	.navbar-content {
		position: relative;
		min-height: calc(100vh - 50px);
	}
	.navbar {
        display: flex;
        justify-content: center;
        align-items: center;
        position: absolute;
        bottom: 0;
        width: 100%;
        
    }
    .navbar-item {
  margin-left: 20px;
  font-size: 20px;
	}
</style>
