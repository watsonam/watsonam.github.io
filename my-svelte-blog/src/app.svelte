<script>
	import Blog from "./routes/blog/+blog.svelte";
	import About from "./routes/about/+about.svelte";
	import LandingPage from "./landing-page.svelte";
	import { onMount } from "svelte";
	let currentPage;

	onMount(() => {
		currentPage = window.location.pathname;
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
