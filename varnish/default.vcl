vcl 4.0;

import directors;

backend user1 {
  .host = "users";
  .port = "8000";
}


backend user2 {
  .host = "usersreplica";
  .port = "8000";
}

backend relation1 {
  .host = "relations";
  .port = "8000";
}

backend relation2 {
  .host = "relationsreplica";
  .port = "8000";
}

backend ads1 {
  .host = "advertisement";
  .port = "8000";
}

backend ads2 {
  .host = "advertisementreplica";
  .port = "8000";
}  


sub vcl_init {
  new user = directors.round_robin();
  user.add_backend(user1);
  user.add_backend(user2);
  
  new relation = directors.round_robin();
  relation.add_backend(relation1);
  relation.add_backend(relation2);

  new ads = directors.round_robin();
  ads.add_backend(ads1);
  ads.add_backend(ads2);
}


sub vcl_recv {
  if (req.url ~ "^/register" || req.url ~ "^/login" || req.url ~ "^/public" || req.url ~ "^/mail" || req.url ~ "^/change") {
    set req.backend_hint = user.backend();
  }
  elseif (req.url ~ "^/add" || req.url ~ "^/following" || req.url ~ "^/followers") {
    set req.backend_hint = relation.backend();
  }
  elseif (req.url ~ "^/advertisements" || req.url ~ "^/categories" || req.url ~ "^/users") {
    set req.backend_hint = ads.backend();
  }


  if ((req.url ~ "^/public_data/" || req.url ~ "^/mail/"|| req.url ~ "^/categories/" || 
      req.url ~ "^/following/" || req.url ~ "^/followers/" || req.url ~ "^/users/\d" || req.url ~ "^/advertisements/popular") && req.method == "GET") {
    

        
        # Strip the cookies
        unset req.http.cookie;
        
        return(hash);
    } else {
        return(pass);
    }

}

sub vcl_backend_response {

    if (bereq.url ~ "^/public_data/" || bereq.url ~ "^/mail/"  || bereq.url ~ "^/categories/" || 
      bereq.url ~ "^/following/" || bereq.url ~ "^/followers/" || bereq.url ~ "^/users/\d" || bereq.url ~ "^/advertisements/popular") {
        set beresp.ttl = 30s;
        set beresp.http.Cache-Control = "max-age=30";
        unset beresp.http.set-cookie;
        unset beresp.http.Pragma;
        unset beresp.http.Expires;
    }
    elseif ( bereq.url ~ "^/advertisements/"|| bereq.url ~ "^/users/") {
        unset beresp.http.Cache-Control;
        set beresp.http.Cache-Control = "private, max-age=30";
        set beresp.http.Vary = "Authorization";
        set beresp.ttl = 30s;
    }
    
    # dont cache redirects and errors
    if (beresp.status >= 300) {
        set beresp.uncacheable = true;
        set beresp.ttl = 30s;
        return (deliver);
    }
    # …
    return (deliver);
}

