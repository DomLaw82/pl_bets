FROM httpd:2.4

COPY ./views /usr/local/apache2/htdocs/static
COPY ./stylesheets /usr/local/apache2/htdocs/static/stylesheets
COPY ./javascripts /usr/local/apache2/htdocs/static/javascripts
COPY ./assets /usr/local/apache2/htdocs/static/assets

RUN sed -i 's#DocumentRoot "/usr/local/apache2/htdocs"#DocumentRoot "/usr/local/apache2/htdocs/static"#' /usr/local/apache2/conf/httpd.conf

EXPOSE 3000