# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: messages.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0emessages.proto\x12\x0ftictactoeserver\"\x1f\n\x11\x43onnectionRequest\x12\n\n\x02id\x18\x01 \x01(\t\"~\n\x0ePlayerResponse\x12%\n\x05point\x18\x01 \x01(\x0b\x32\x16.tictactoeserver.Point\x12-\n\tcharacter\x18\x02 \x01(\x0e\x32\x1a.tictactoeserver.Character\x12\x16\n\x0e\x63ount_of_users\x18\x03 \x01(\x05\"@\n\x0bMoveRequest\x12\n\n\x02id\x18\x01 \x01(\t\x12%\n\x05point\x18\x02 \x01(\x0b\x32\x16.tictactoeserver.Point\"0\n\x0cMoveResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\"\x1d\n\x05Point\x12\t\n\x01x\x18\x01 \x01(\x05\x12\t\n\x01y\x18\x02 \x01(\x05*$\n\tCharacter\x12\x05\n\x01X\x10\x00\x12\x05\n\x01O\x10\x01\x12\t\n\x05\x45MPTY\x10\x02\x32\xa7\x01\n\x04Game\x12R\n\x07\x63onnect\x12\".tictactoeserver.ConnectionRequest\x1a\x1f.tictactoeserver.PlayerResponse\"\x00\x30\x01\x12K\n\x08makeMove\x12\x1c.tictactoeserver.MoveRequest\x1a\x1d.tictactoeserver.MoveResponse\"\x00(\x01\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'messages_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _CHARACTER._serialized_start=343
  _CHARACTER._serialized_end=379
  _CONNECTIONREQUEST._serialized_start=35
  _CONNECTIONREQUEST._serialized_end=66
  _PLAYERRESPONSE._serialized_start=68
  _PLAYERRESPONSE._serialized_end=194
  _MOVEREQUEST._serialized_start=196
  _MOVEREQUEST._serialized_end=260
  _MOVERESPONSE._serialized_start=262
  _MOVERESPONSE._serialized_end=310
  _POINT._serialized_start=312
  _POINT._serialized_end=341
  _GAME._serialized_start=382
  _GAME._serialized_end=549
# @@protoc_insertion_point(module_scope)
