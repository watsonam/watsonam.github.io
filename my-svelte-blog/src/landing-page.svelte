<script>
    import Navbar from "./navbar.svelte";

</script>
<link
	href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;700&display=swap"
	rel="stylesheet"
/>

<Navbar></Navbar>
<div class="container">
	<img src="./me.jpg" alt="Adam Watson" class="profile-image" />
	<h1>Adam Watson</h1>
	<div class="social-links">
		<a href='https://github.com/yourusername' target='_blank' rel="noreferrer">
			<img src='https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg' alt='GitHub' class='social-logo'/>
			<span>GitHub</span>
		  </a>
		  <a href='https://twitter.com/AdamWat73946377' target='_blank' rel="noreferrer">
			<img src='https://upload.wikimedia.org/wikipedia/commons/4/4f/Twitter-logo.svg' alt='Twitter' class='social-logo'/>
			<span>Twitter</span>
		  </a>
		  <a href='https://www.linkedin.com/in/adam-watson-9831a099/' target='_blank' rel="noreferrer">
			<img src='https://upload.wikimedia.org/wikipedia/commons/8/81/LinkedIn_icon.svg' alt='LinkedIn' class='social-logo'/>
			<span>LinkedIn</span>
		  </a>
		  
	</div>
	<div class="about-me">
		<p>
			A personal blog, not taken too seriously, for any rambling thoughts,
			travel posts and technical write ups.
		</p>
		<p>Get in touch at adam.watson1994@hotmail.co.uk</p>
	</div>
</div>

<style>
	/* Styles for the landing page */
	.container {
		display: flex;
		flex-direction: column;
		align-items: center;
		font-family: "Open Sans", sans-serif;
	}
	.profile-image {
		width: 150px;
		width: 150px;
		border-radius: 50%;
		margin-top: 100px;
		margin-bottom: 15px;
		box-shadow: 0 0 0 0 #677d00, 0 0 0 white, 0em 0em 0 0em #acd373, 0.1em 0.1em 0em 0.2em #677d00;
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
	.social-logo {
    width: 25px;
    height: 25px;
    vertical-align: middle;
    margin-right: 10px;
}

</style>
