Base.html

```html
{% load static %}

<!DOCTYPE HTML>
<html>
  <head>
    {% block head %}
      
	{% endblock %}
  </head>

  <body class="bg-secondary">
    <!-- MY SCRIPTS-->

    <!-- CONTENT -->
    <article>
      <div id="PAGE" class="container-fluid ">
        <!-- MODAL -->
        <div id="MODAL" class="modal fade">
          
        </div>
        <!-- FILTERS -->
        <div id="FILTERS" class="row fixed-top bg-dark p-1">
          
        </div>
        <!-- DATAS_TO_DISPLAY -->
        <div id="DATAS">
          
        </div>
      </div>
    </article>

    <!-- TOP MENU BAR -->
    {% block menu %}
      
	{% endblock %}
    <!-- COMMON SCRIPTS -->
    
    <!-- LAUNCH SCRIPT AFTER LOAD -->
    
  </body>
</html>

```

Head

```html
{% extends 'appname/base.html' %}

{% block head %}
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="stylesheet" href="../tools/bootstrap.min.css">
	<!-- ICONS -->
	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
	<link rel="stylesheet" href="../css/<?=$page_name?>.css?<?php echo time(); ?>">
    <title>Summary</title>
{% endblock head %}
```

Menu

```html
{% extends 'appname/base.html' %}

{% block menu %}
<nav id="MENU_nav" class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
  <a class="navbar-brand" href="#">Menu</a>
  <span class="navbar-text mx-3 font-italic">
    <?php echo "Page: <kbd>".$_SESSION['mypage']."</kbd>"; ?>
  </span>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#collapsibleNavbar">
      <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="collapsibleNavbar">
    <ul class="navbar-nav">
    	<li class="nav-item"><a class="nav-link" href="../pages/import.php">Import</a></li>
    	<li class="nav-item"><a class="nav-link" href="../pages/summary.php">Acceuil</a></li>
    	<li class="nav-item"><a class="nav-link" href="../pages/details.php">Détails</a></li>
    	<li class="nav-item"><a class="nav-link" href="../pages/month_chart.php">Graphs Mois</a></li>
    	<li class="nav-item"><a class="nav-link" href="../pages/year_chart.php">Graphs YTD</a></li>
    	<li class="nav-item"><a class="nav-link" href="../pages/budget.php">Budget</a></li>
    	<li class="nav-item"><a class="nav-link" href="../pages/epargne.php">Epargne</a></li>
      <li class="nav-item"><a class="nav-link" href="#">#</a></li>
    	<li class="nav-item"><a class="nav-link" href="../login.php">Disconnect</a></li>
    </ul>
  </div>

</nav>
{% endblock menu %}
```

