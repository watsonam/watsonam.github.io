
<script>
  import { onMount } from 'svelte';

  let articles = [
    { year: 2022, text: '/articles/test-blog.md' },
  ];

  onMount(async () => {
    // Fetch the markdown text for each article
    articles = await Promise.all(articles.map(async (article) => {
      try {
        const response = await fetch(article.text);
        article.text = await response.text();
        return article;
      } catch (error) {
        console.error(error);
      }
    }));
  });
</script>


<div class="articles">
  {#each articles as article}
    <div class="article">
      <div class="year">{article.year}</div>
      <div>{article.text}</div>
    </div>
  {/each}
</div>

<style>
  /* Styles for the blog page */
  .articles {
    display: flex;
    flex-wrap: wrap;
  }

  .article {
    width: 100%;
    margin-bottom: 2rem;
    padding: 1rem;
    box-sizing: border-box;
  }

  .year {
    font-size: 1.5rem;
    font-weight: bold;
    margin-right: 1rem;
  }
</style>