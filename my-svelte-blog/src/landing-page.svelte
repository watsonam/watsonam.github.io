<link
	href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;700&display=swap"
	rel="stylesheet"
/>

<div class="container">
	<!-- <img src={logo} alt="Adam Watson" /> -->
	<h1>Adam Watson</h1>
	<div class="social-links">
		<a href="https://github.com/adamwatson">Github</a>
		<a href="https://linkedin.com/in/adamwatson">LinkedIn</a>
		<a href="https://twitter.com/adamwatson">Twitter</a>
	</div>
	<div class="about-me">
		<p>
			A personal blog, not taken too seriously, for any rambling thoughts,
			travel posts and technical write ups. This website was built using
			Amazon Lightsail where a WordPress site is launched on a virtual
			server. I have not enjoyed working with WordPress! However, if time
			is of the essence and you want to quickly host a website with your
			own content, then this isn’t a bad start.
		</p>
	</div>
</div>

<!-- <Navbar /> -->
<style>
	/* Styles for the landing page */
	.container {
		display: flex;
		flex-direction: column;
		align-items: center;
		font-family: "Open Sans", sans-serif;
	}

	.about-me {
		text-align: center;
		font-size: 25px;
		margin-left: 300px;
		margin-right: 300px;
	}

	h1 {
		font-size: 3rem;
		margin-top: 3rem;
	}

	.social-links {
		display: flex;
	}

	.social-links a {
		margin-right: 1rem;
	}
</style>
