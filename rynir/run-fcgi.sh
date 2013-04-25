#!/bin/bash
BASEDIR=$(cd ..; pwd)
kill $(cat $BASEDIR/data/rynir.pid)
rm -f $BASEDIR/data/rynir.{pid,sock}
exec ./rynir-www.py runfcgi \
  method=prefork \
  maxrequests=200 \
  maxspare=10 \
  minspare=5 \
  maxchildren=25 \
  pidfile=$BASEDIR/data/rynir.pid \
  socket=$BASEDIR/data/rynir.sock \
  outlog=$BASEDIR/data/rynir-www.log \
  errlog=$BASEDIR/data/rynir-www.err \
  debug=true \
  "$@"
