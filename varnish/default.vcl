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
  if (req.url ~ "^/users/") {
    set req.url = regsub(req.url,"^/users", "");
    set req.backend_hint = user.backend();
  }
  elseif (req.url ~ "^/relations/") {
    set req.url = regsub(req.url,"^/relations", "");
    set req.backend_hint = relation.backend();
  }
  elseif (req.url ~ "^/ads/") {
    set req.url = regsub(req.url,"^/ads", "");
    set req.backend_hint = ads.backend();
  }


  if ((req.url ~ "^/public_data/"
    ) && req.method == "GET") {
    

        
        # Strip the cookies
        unset req.http.cookie;
        
        return(hash);
    } else {
        return(pass);
    }

}

sub vcl_backend_response {

    if (bereq.url ~ "^/public_data/"
    ){
        set beresp.ttl = 30s;
        unset beresp.http.set-cookie;
        unset beresp.http.Pragma;
        unset beresp.http.Expires;
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

